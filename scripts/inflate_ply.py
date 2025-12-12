#!/usr/bin/env python3
import numpy as np
import sys

def inflate_ply(input_path, output_path, scale_ratio):
    vertices = []
    header = []
    faces = []
    in_vertex_section = False
    vertex_count = 0
    read_vertices = 0

    # === Read PLY ===
    with open(input_path, "r") as f:
        for line in f:
            header.append(line)
            if line.startswith("element vertex"):
                vertex_count = int(line.split()[-1])
            if line.strip() == "end_header":
                break

        # Read vertex lines
        for _ in range(vertex_count):
            x, y, z = map(float, f.readline().split()[:3])
            vertices.append([x, y, z])
        # Read faces if exist
        for line in f:
            faces.append(line)

    vertices = np.array(vertices)
    centroid = vertices.mean(axis=0)

    # === Inflate ===
    # (v - c) * (0 + scale_ratio) + c
    inflated = (vertices - centroid) * (0 + scale_ratio) + centroid

    # === Write PLY ===
    with open(output_path, "w") as f:
        # headerそのまま
        for h in header:
            f.write(h)
        # vertices
        for v in inflated:
            f.write(f"{v[0]} {v[1]} {v[2]}\n")
        # faces
        for face in faces:
            f.write(face)

    print(f"Saved inflated ply → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python inflate_ply.py input.ply output.ply scale_ratio")
        print("Example: python inflate_ply.py in.ply out.ply 1.05   # 5% inflate")
        sys.exit(1)

    inflate_ply(sys.argv[1], sys.argv[2], float(sys.argv[3]))
