import argparse
from PIL import Image, ImageFilter, ImageOps
import numpy as np
import os


def process_image(input_path, output_dir, threshold_dark=60, median_filter_size=3, background="white"):
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Load and prepare image with chosen background color
    image = Image.open(input_path).convert("RGBA")
    bg_color = "WHITE" if background.lower() == "white" else "BLACK"
    base_bg = Image.new("RGBA", image.size, bg_color)
    base_bg.paste(image, (0, 0), mask=image)
    original_rgb = base_bg.convert("RGB")
    gray = base_bg.convert("L")

    # Step 2: Extract dark features (pure black and white using low threshold)
    bw_dark = gray.point(lambda p: 255 if p > threshold_dark else 0, mode='1')
    bw_dark_path = os.path.join(output_dir, "step1_dark_features_bw.bmp")
    bw_dark.save(bw_dark_path)

    # Step 3: Subtract dark features from original to keep only color
    mask_np = np.array(bw_dark.convert("L")) == 0
    original_np = np.array(original_rgb)
    color_only_np = original_np.copy()
    color_only_np[mask_np] = [255, 255, 255] if background.lower() == "white" else [0, 0, 0]
    color_only_img = Image.fromarray(color_only_np)
    color_only_path = os.path.join(output_dir, "step2_color_only.bmp")
    color_only_img.save(color_only_path)

    # Step 4: Smooth and apply dithering (halftone)
    color_gray = color_only_img.convert("L")
    smoothed = color_gray.filter(ImageFilter.MedianFilter(size=median_filter_size))
    dithered = smoothed.convert("1")  # Floyd–Steinberg dithering
    dithered_path = os.path.join(output_dir, "step3_dithered_color_only.bmp")
    dithered.save(dithered_path)

    # Step 5: Restore black lines
    bw_dark_rgb = bw_dark.convert("RGB")
    dithered_rgb = dithered.convert("RGB")
    final_combined = dithered_rgb.copy()
    final_pixels = final_combined.load()
    dark_pixels = bw_dark_rgb.load()

    for y in range(final_combined.height):
        for x in range(final_combined.width):
            if dark_pixels[x, y] == (0, 0, 0):
                final_pixels[x, y] = (0, 0, 0)

    final_path = os.path.join(output_dir, "step4_final_combined.bmp")
    final_combined.save(final_path)

    # Step 6: Invert the final image
    inverted = ImageOps.invert(final_combined.convert("L"))
    inverted_path = os.path.join(output_dir, "step5_inverted.bmp")
    inverted.save(inverted_path)

    return {
        "dark_features": bw_dark_path,
        "color_only": color_only_path,
        "dithered": dithered_path,
        "final_combined": final_path,
        "inverted": inverted_path
    }


def main():
    parser = argparse.ArgumentParser(description="Process an image to extract dark features and apply dithered halftone.")
    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("output", help="Directory to save the output steps")
    parser.add_argument("--threshold", type=int, default=60, help="Threshold for detecting dark features (default: 60)")
    parser.add_argument("--filter", type=int, default=3, help="Median filter size for smoothing (default: 3)")
    parser.add_argument("--background", choices=["white", "black"], default="white", help="Background color to apply behind transparent areas (default: white)")
    args = parser.parse_args()

    results = process_image(
        args.input,
        args.output,
        threshold_dark=args.threshold,
        median_filter_size=args.filter,
        background=args.background
    )

    print("Processing complete. Files saved:")
    for key, path in results.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()

