import argparse
from PIL import Image, ImageFilter, ImageOps
import numpy as np
import os


def process_image(input_path, output_dir, threshold_dark=60, median_filter_size=3, background="white", invert=False):
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Load and prepare image with chosen background color
    image = Image.open(input_path).convert("RGBA")
    if invert:
        image = ImageOps.invert(image.convert("RGB")).convert("RGBA")

    bg_color = "WHITE" if background.lower() == "white" else "BLACK"
    base_bg = Image.new("RGBA", image.size, bg_color)
    base_bg.paste(image, (0, 0), mask=image)
    original_rgb = base_bg.convert("RGB")
    gray = base_bg.convert("L")

    # Step 2: Extract features using threshold
    if invert:
        bw_feature_mask = gray.point(lambda p: 0 if p > threshold_dark else 255, mode='1')  # keep light
    else:
        bw_feature_mask = gray.point(lambda p: 255 if p > threshold_dark else 0, mode='1')  # keep dark
    bw_mask_path = os.path.join(output_dir, "step1_features_mask.bmp")
    bw_feature_mask.save(bw_mask_path)

    # Step 3: Subtract features from original to keep only color
    mask_np = np.array(bw_feature_mask.convert("L")) == 0
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

    # Step 5: Restore features (black or white lines depending on inversion)
    feature_mask_rgb = bw_feature_mask.convert("RGB")
    dithered_rgb = dithered.convert("RGB")
    final_combined = dithered_rgb.copy()
    final_pixels = final_combined.load()
    mask_pixels = feature_mask_rgb.load()

    for y in range(final_combined.height):
        for x in range(final_combined.width):
            if mask_pixels[x, y] == (0, 0, 0):
                final_pixels[x, y] = (255, 255, 255) if invert else (0, 0, 0)

    final_path = os.path.join(output_dir, "step4_final_combined.bmp")
    final_combined.save(final_path)

    return {
        "feature_mask": bw_mask_path,
        "color_only": color_only_path,
        "dithered": dithered_path,
        "final_combined": final_path
    }


def main():
    parser = argparse.ArgumentParser(description="Process an image to extract features and apply dithered halftone.")
    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("output", help="Directory to save the output steps")
    parser.add_argument("--threshold", type=int, default=60, help="Threshold for detecting features (default: 60)")
    parser.add_argument("--filter", type=int, default=3, help="Median filter size for smoothing (default: 3)")
    parser.add_argument("--background", choices=["white", "black"], default="white", help="Background color to apply behind transparent areas (default: white)")
    parser.add_argument("--invert", action="store_true", help="Invert the input image before processing")
    args = parser.parse_args()

    results = process_image(
        args.input,
        args.output,
        threshold_dark=args.threshold,
        median_filter_size=args.filter,
        background=args.background,
        invert=args.invert
    )

    print("Processing complete. Files saved:")
    for key, path in results.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
