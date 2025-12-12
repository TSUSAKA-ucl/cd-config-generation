#!/usr/bin/env python3
"""
truncate the bounding box of a mesh by cutting off its edges and corners at 45 degrees,
and output the new vertex coordinates to a CSV file.
"""
import sys
import argparse
import csv

def read_truncate_write():
    """
    Read bounding box data from stdin, truncate it, and write new vertex coordinates to a CSV file.
    """
    parser = argparse.ArgumentParser(description="truncate bounding box and output vertex coordinates to CSV")
    parser.add_argument('-i', '--input', type=str,
                        help="input source filename. if not specified, use standard input.")
    parser.add_argument('-o', '--output', type=str,
                        default="truncatedBBox.csv",
                        help="output CSV filename. (default: truncatedBBox.csv)")
    parser.add_argument('-s', '--scale', type=float, default=1.0,
                        help="scale factor. (default: 1.0)")

    args = parser.parse_args()
                        

    # 入力ソースを決定
    if args.input:
        try:
            f = open(args.input, 'r', encoding='utf-8')
        except IOError as e:
            print(f"can't open: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        f = sys.stdin

    scale = args.scale


    # read all lines from stdin, ignoring empty lines
    lines = [line.strip() for line in f if line.strip()]
    if not lines:
        print("no input data.", file=sys.stderr)
        return

    # "Mesh Bounding Box min/max" 行を抽出して数値化
    scale_xyz = [1,1,1]
    for line in lines:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "Mesh" and parts[1] == "Bounding" and parts[2] == "Box":
            print('found bounding box data:', line, file=sys.stderr)
            if parts[3] == "min":
                try:
                    min_xyz = list(map(float, parts[4:7]))
                except ValueError:
                    print(f"invalid number data: {line}", file=sys.stderr)
            if parts[3] == "max":
                try:
                    max_xyz = list(map(float, parts[4:7]))
                except ValueError:
                    print(f"invalid number data: {line}", file=sys.stderr)
            if parts[3] == "Size":
                try:
                    size_xyz = list(map(float, parts[4:7]))
                except ValueError:
                    print(f"invalid number data: {line}", file=sys.stderr)
            if parts[3] == "crop":
                try:
                    crop_xyz = list(map(float, parts[4:7]))
                except ValueError:
                    print(f"invalid number data: {line}", file=sys.stderr)
            if parts[3] == "scale":
                print('found scale data:', line, file=sys.stderr)
                try:
                    scale_xyz = list(map(float, parts[4:7]))
                    print('scale_xyz:', scale_xyz, file=sys.stderr)
                    # if scale != 1.0:
                    #     scale = min(scale_xyz)
                except ValueError:
                    print(f"invalid number data: {line}", file=sys.stderr)
    print('OUTER scale_xyz:', scale_xyz, file=sys.stderr)
    if 'min_xyz' not in locals() or 'max_xyz' not in locals():
        print("can't find bounding box data.", file=sys.stderr)
        return
    if 'size_xyz' in locals() and 'crop_xyz' in locals():
        max_xyz = list(map(lambda i: 0.5*((1+crop_xyz[i])*max_xyz[i]+(1-crop_xyz[i])*(min_xyz[i]+size_xyz[i])), range(3)))
        min_xyz = list(map(lambda i: max_xyz[i]-size_xyz[i], range(3)))

    print('modified min_xyz:', min_xyz, file=sys.stderr)
    print('modified max_xyz:', max_xyz, file=sys.stderr)
    #size_xyz = [max_xyz[i] - min_xyz[i] for i in range(3)]
    # truncate_size = min(size_xyz) * .29289321881345247560*scale
    width_xyz = list(map(lambda i: (max_xyz[i] - min_xyz[i]) * scale_xyz[i], range(3)))
    print('width_xyz:', width_xyz, file=sys.stderr)
    truncate_size = list(map(lambda i: width_xyz[i] * .29289321881345247560, range(3)))
    print('truncate_size:', truncate_size, file=sys.stderr)
    x_min = min_xyz[0]
    x_max = max_xyz[0]
    y_min = min_xyz[1]
    y_max = max_xyz[1]
    z_min = min_xyz[2]
    z_max = max_xyz[2]

    x_min_trunc = min_xyz[0] + truncate_size[0]
    x_max_trunc = max_xyz[0] - truncate_size[0]
    y_min_trunc = min_xyz[1] + truncate_size[1]
    y_max_trunc = max_xyz[1] - truncate_size[1]
    z_min_trunc = min_xyz[2] + truncate_size[2]
    z_max_trunc = max_xyz[2] - truncate_size[2]
    data = [
        [x_min, y_min_trunc, z_min_trunc],
        [x_min, y_max_trunc, z_min_trunc],
        [x_min, y_min_trunc, z_max_trunc],
        [x_min, y_max_trunc, z_max_trunc],

        [x_min_trunc, y_min, z_min_trunc],
        [x_min_trunc, y_max, z_min_trunc],
        [x_min_trunc, y_min, z_max_trunc],
        [x_min_trunc, y_max, z_max_trunc],
        [x_min_trunc, y_min_trunc, z_min],
        [x_min_trunc, y_max_trunc, z_min],
        [x_min_trunc, y_min_trunc, z_max],
        [x_min_trunc, y_max_trunc, z_max],

        [x_max_trunc, y_min, z_min_trunc],
        [x_max_trunc, y_max, z_min_trunc],
        [x_max_trunc, y_min, z_max_trunc],
        [x_max_trunc, y_max, z_max_trunc],
        [x_max_trunc, y_min_trunc, z_min],
        [x_max_trunc, y_max_trunc, z_min],
        [x_max_trunc, y_min_trunc, z_max],
        [x_max_trunc, y_max_trunc, z_max],

        [x_max, y_min_trunc, z_min_trunc],
        [x_max, y_max_trunc, z_min_trunc],
        [x_max, y_min_trunc, z_max_trunc],
        [x_max, y_max_trunc, z_max_trunc]
        ]
    # CSVファイルに出力
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # writer.writerow(["X", "Y", "Z"])
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    read_truncate_write()
