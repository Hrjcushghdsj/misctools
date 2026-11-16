"""
Generate an SVG squircle (superellipse) shape.

This script creates a vector graphic of a squircle - a shape intermediate between
a circle and a square - defined by the superellipse equation. The shape's "roundness"
is controlled by an exponent parameter n, where n=2 produces a perfect circle,
n=4 yields a classic squircle, and larger values approach a square with rounded
corners.

The generated SVG uses a closed path constructed from discrete points sampled
around the perimeter, offering a balance between geometric accuracy and
computational simplicity. The output can be customized in size, exponent, and
filename via command-line arguments.

Usage examples:
    python generate_squircle.py -o squircle.svg                 # Default: n=4, 512px square
    python generate_squircle.py -e 3.5 -s 256 -o squircle.svg   # Custom exponent and size
    python generate_squircle.py -e 6 -o squircle.svg            # More square-like shape
"""
import argparse
import numpy as np
import svgwrite

def generate_squircle_path(n, width, height, num_points=300):
    a = width / 2
    b = height / 2
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = a * np.sign(np.cos(theta)) * np.abs(np.cos(theta))**(2 / n)
    y = b * np.sign(np.sin(theta)) * np.abs(np.sin(theta))**(2 / n)
    points = np.column_stack([x + width / 2, y + height / 2])
    return points

def save_svg(points, width, height, output_file):
    dwg = svgwrite.Drawing(output_file, size=(f"{width}px", f"{height}px"))
    path_data = f"M {points[0][0]},{points[0][1]} " + " ".join(
        [f"L {x},{y}" for x, y in points[1:]]
    ) + " Z"
    dwg.add(dwg.path(d=path_data, fill="black"))
    dwg.save()

def main():
    parser = argparse.ArgumentParser(description="Generate a squircle SVG.")
    parser.add_argument("-e", "--exponent", type=float, default=4.0, help="Exponent n for the superellipse (e.g., 2 = circle, 4 = squircle)")
    parser.add_argument("-s", "--size", type=int, default=512, help="Size of the squircle in pixels")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output SVG filename")
    args = parser.parse_args()

    points = generate_squircle_path(args.exponent, args.size, args.size)
    save_svg(points, args.size, args.size, args.output)
    print(f"Saved squircle to {args.output}")

if __name__ == "__main__":
    main()
