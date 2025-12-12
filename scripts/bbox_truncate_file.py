#!/usr/bin/env python3
"""
truncate the bounding box of a mesh by cutting off its edges and corners at 45 degrees,
and output the new vertex coordinates to a CSV file.
"""
import sys
import csv

def read_truncate_write():
  """
  Read bounding box data from stdin, truncate it, and write new vertex coordinates to a CSV file.
  """
  # read all lines from stdin, ignoring empty lines
  with open("bbox.txt", "r") as bbox:
    lines = [line.strip() for line in bbox if line.strip()]
    if not lines:
        print("no input data.", file=sys.stderr)
        return

    # "Mesh Bounding Box min/max" 行を抽出して数値化
    for line in lines:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "Mesh" and parts[1] == "Bounding" and parts[2] == "Box":
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
    if 'min_xyz' not in locals() or 'max_xyz' not in locals():
        print("can't find bounding box data.", file=sys.stderr)
        return

    size_xyz = [max_xyz[i] - min_xyz[i] for i in range(3)]
    truncate_size = min(size_xyz) * .29289321881345247560
    x_min = min_xyz[0]
    x_max = max_xyz[0]
    y_min = min_xyz[1]
    y_max = max_xyz[1]
    z_min = min_xyz[2]
    z_max = max_xyz[2]

    x_min_trunc = min_xyz[0] + truncate_size
    x_max_trunc = max_xyz[0] - truncate_size
    y_min_trunc = min_xyz[1] + truncate_size
    y_max_trunc = max_xyz[1] - truncate_size
    z_min_trunc = min_xyz[2] + truncate_size
    z_max_trunc = max_xyz[2] - truncate_size
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
    with open("truncatedBBox.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # writer.writerow(["X", "Y", "Z"])
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    read_truncate_write()
