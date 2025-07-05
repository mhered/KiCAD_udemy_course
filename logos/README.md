# README.md

`make_kicad_logo.py`  is a simple python script that takes an rgba image and generates monochrome bitmaps to use in KiCAD Image converter. The script saves five intermediate steps and allows a few parameters (threshold, color for the transparent background etc) 

Note: high resolution halftone images seem to crash KiCAD (on Ubuntu 24.04 Wayland), see below for `make_kicad_logo_v2.py` (WIP)

--

Example usage:

```bash  
$ python3 make_kicad_logo.py --background black sevillabot_logo_1200.png sevillabot_logo_1200_black
Processing complete. Files saved:
dark_features: sevillabot_logo_1200_black/step1_dark_features_bw.bmp
color_only: sevillabot_logo_1200_black/step2_color_only.bmp
dithered: sevillabot_logo_1200_black/step3_dithered_color_only.bmp
final_combined: sevillabot_logo_1200_black/step4_final_combined.bmp
inverted: sevillabot_logo_1200_black/step5_inverted.bmp
```

Help:
```bash
$ python3 make_kicad_logo.py --help
usage: make_kicad_logo.py [-h] [--threshold THRESHOLD] [--filter FILTER]
                          [--background {white,black}]
                          input output

Process an image to extract dark features and apply dithered halftone.

positional arguments:
  input                 Path to the input image
  output                Directory to save the output steps

options:
  -h, --help            show this help message and exit
  --threshold THRESHOLD
                        Threshold for detecting dark features (default: 60)
  --filter FILTER       Median filter size for smoothing (default: 3)
  --background {white,black}
                        Background color to apply behind transparent areas
                        (default: white)
```

## WIP

- [ ] Modify script (see `make_kicad_logo_v2.py`) because KiCAD Image Converter converts the halftone to vector image made of filled polygons, it takes ages and the result is a huge file. What is confusing is that black dots are printed white on the PCB!. Input image should be reversed and made of black dots over white bkg. May need to play with contrast? The new version takes --invert parameter to invert at the beginning, but that changes all the logic. Not sure it works well, in any case the images are still huge.
