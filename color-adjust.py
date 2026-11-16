"""
Replace all colors in an image with a specified hex color while preserving alpha transparency.

For each pixel in the input image, the RGB channels are replaced entirely with the target color.
The alpha channel is either preserved as-is or optionally clamped based on a threshold:
- Without --alpha-threshold: original alpha values are kept unchanged.
- With --alpha-threshold: pixels with alpha below the given percentage (0-100) become fully transparent (0),
  while those at or above the threshold become fully opaque (255).

Useful for creating monochromatic versions of images, generating color overlays, or masking
images with a single color while controlling transparency cutoffs.
"""
import argparse
from PIL import Image


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Hex color must be 6 digits long.")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def replace_colors(image_path, output_path, new_color, alpha_threshold=None):
    image = Image.open(image_path).convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if alpha_threshold is not None:
                if a < int((alpha_threshold / 100) * 255):
                    a = 0
                else:
                    a = 255
            pixels[x, y] = (*new_color, a)  # Replace RGB, keep alpha

    image.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Replace image colors with a specific hex color, preserving alpha.")
    parser.add_argument('-f', '--file', required=True, help="Input image file path")
    parser.add_argument('-o', '--output', required=True, help="Output image file path")
    parser.add_argument('-c', '--color', required=True, help="Hex color code (e.g., #ff0000)")
    parser.add_argument('-a', '--alpha-threshold', type=int, help="Alpha threshold percentage (0-100). If specified, pixels with alpha below threshold are set to 0, others to 255.")

    args = parser.parse_args()

    try:
        new_rgb = hex_to_rgb(args.color)
        replace_colors(args.file, args.output, new_rgb, args.alpha_threshold)
        print(f"Image saved to {args.output} with color {args.color}.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()