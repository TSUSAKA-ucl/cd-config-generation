import sys
import csv
import numpy as np
from scipy.spatial import ConvexHull
import trimesh

with open(sys.argv[1]) as f:
    points = [[float(str) for str in row] for row in csv.reader(f)]
    hull = ConvexHull(points)
    mesh = trimesh.Trimesh(vertices=points, faces=hull.simplices)
    mesh.export('convex_hull.stl')
