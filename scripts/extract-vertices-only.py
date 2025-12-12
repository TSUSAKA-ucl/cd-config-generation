from stl import mesh
import numpy as np

m = mesh.Mesh.from_file("input.stl")
vertices = np.unique(m.vectors.reshape(-1,3), axis=0)

# PLY ASCII
with open("vertices.ply", "w") as f:
    f.write("ply\nformat ascii 1.0\n")
    f.write(f"element vertex {len(vertices)}\n")
    f.write("property float x\nproperty float y\nproperty float z\n")
    f.write("end_header\n")
    for v in vertices:
        f.write(f"{v[0]} {v[1]} {v[2]}\n")
