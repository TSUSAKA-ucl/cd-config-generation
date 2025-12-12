#!/bin/bash
# Construct a MeshLab project XML file including only those meshes
echo '<!DOCTYPE MeshLabDocument>'
echo '<MeshLabProject>'
echo ' <MeshGroup>'
while [ $# -ge 1 ]
do Fname="$1"
   # read elStr vtxStr NumVertex <<<`grep vertex "$1"`
   # if [ "$elStr" = element ] && [ "$vtxStr" = "vertex" ] &&\
   # 	  [ "$NumVertex" -gt 3 ]; then
   # Select only convex objects with a volume of 2 cubic millimeters or more
   if python3 - <<EOF "$1" 1>&2
import sys
import trimesh
def stable_volume(mesh):
    # 1) mesh が閉じてなければ体積ゼロ
    if not mesh.is_volume:
        return 0.0

    raw = mesh.volume

    # 2) AABB 寸法による相対閾値
    bbox = mesh.bounds
    diag = ((bbox[1] - bbox[0])**2).sum()**0.5
    vmin = (diag ** 3) * 1e-12

    # 3) 閾値以下なら誤差として捨てる
    if raw < vmin:
        return 0.0

    return raw

mesh = trimesh.load(sys.argv[1])
volume = stable_volume(mesh)
print(f"{sys.argv[1]} volume: {volume*1e9:12.1f} cubic millimeters, convex: {mesh.is_convex}")
if volume >= 2e-9: # and mesh.is_convex:
   sys.exit(0)
else:
   sys.exit(1)
EOF
   then
       Label=`basename "$1"`
       echo '  <MLMesh label="'"$Label"'" visible="1" filename="'"$Fname"'">'
       cat <<EOF
   <MLMatrix44>
1 0 0 0 
0 1 0 0 
0 0 1 0 
0 0 0 1 
</MLMatrix44>
   <RenderingOption pointColor="131 149 69 255" wireColor="64 64 64 255" solidColor="192 192 192 255" boxColor="234 234 234 255" pointSize="3" wireWidth="1">100001000100000000000000000001010100100010100000000100111011110000001001</RenderingOption>
  </MLMesh>
EOF
   fi
   shift
done
echo ' </MeshGroup>'
echo ' <RasterGroup/>'
echo '</MeshLabProject>'
