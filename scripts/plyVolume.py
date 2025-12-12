import sys
import trimesh
mesh = trimesh.load(sys.argv[1])
volume = mesh.volume
print(f"{sys.argv[1]} volume: {volume*1e9:12.1f} cubic millimeters")
if volume >= 2e-9 and mesh.is_convex:
   sys.exit(0)
else:
   sys.exit(1)
