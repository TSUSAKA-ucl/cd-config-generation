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
    half = list(map(lambda i: (max_xyz[i] - min_xyz[i])/2, range(3)))
    center = list(map(lambda i: (max_xyz[i] + min_xyz[i])/2, range(3)))
    print('half:', half, file=sys.stderr)
    # c_xyz[0] = half[1] > half[2] ? half[2] : half[1]
    c_xyz = [0,0,0]
    c_xyz[0] = half[1] if half[1] < half[2] else half[2]
    c_xyz[1] = half[2] if half[2] < half[0] else half[0]
    c_xyz[2] = half[0] if half[0] < half[1] else half[1]
    chamfer = list(map(lambda i: c_xyz[i] * .58578643762690495120  * scale_xyz[i], range(3)))
    print('chamfer_size:', chamfer, file=sys.stderr)
        # ptA = [half[x]-chamfer[z], half[y]-chamfer[x], half[z]]
        # ptB = [half[x]-chamfer[y], half[y]-chamfer[z], half[z]]
        # ptC = [half[x]-chamfer[z], half[y], half[z]-chamfer[x]]
        # ptD = [half[x], half[y]-chamfer[z], half[z]-chamfer[y]]
    if chamfer[0] > chamfer[1] and chamfer[0] > chamfer[2]:
        print('largest chamfer is X axis', chamfer[0], file=sys.stderr)
        # z->0, x->1, y->2
        ptA = [half[0], half[1]-chamfer[0], half[2]-chamfer[1]]
        ptB = [half[0], half[1]-chamfer[2], half[2]-chamfer[0]]
        ptC = [half[0]-chamfer[1], half[1]-chamfer[0], half[2]]
        ptD = [half[0]-chamfer[2], half[1], half[2]-chamfer[0]]
    elif chamfer[1] > chamfer[2] and chamfer[1] > chamfer[0]:
        print('largest chamfer is Y axis', chamfer[1], file=sys.stderr)
        # z->1, x->2, y->0
        ptA = [half[0]-chamfer[2], half[1], half[2]-chamfer[1]]
        ptB = [half[0]-chamfer[1], half[1], half[2]-chamfer[0]]
        ptC = [half[0], half[1]-chamfer[2], half[2]-chamfer[1]]
        ptD = [half[0]-chamfer[1], half[1]-chamfer[0], half[2]]
    else: # if chamfer[2] > chamfer[0] and chamfer[2] > chamfer[1]:
        print('largest chamfer is Z axis', chamfer[2], file=sys.stderr)
        # z->2, y->1, x->0
        ptA = [half[0]-chamfer[2], half[1]-chamfer[0], half[2]]
        ptB = [half[0]-chamfer[1], half[1]-chamfer[2], half[2]]
        ptC = [half[0]-chamfer[2], half[1], half[2]-chamfer[0]]
        ptD = [half[0], half[1]-chamfer[2], half[2]-chamfer[1]]
    points = [
        [ptA[0], ptA[1], ptA[2]],
        [ptB[0], ptB[1], ptB[2]],
        [ptC[0], ptC[1], ptC[2]],
        [ptD[0], ptD[1], ptD[2]]
    ]
    # x,y,zをそれぞれ符号反転したpointを追加して32点にする
    data = []
    for px in [1, -1]:
        for py in [1, -1]:
            for pz in [1, -1]:
                for pt in points:
                    data.append([px*pt[0]+center[0], py*pt[1]+center[1], pz*pt[2]+center[2]])
    # CSVファイルに出力
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # writer.writerow(["X", "Y", "Z"])
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    read_truncate_write()
