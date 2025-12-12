#!/bin/bash
x=`readlink "$0"`
if [ $? -eq 0 ]
then cd `dirname "$x"`
else cd `dirname "$0"`
fi
ThisDir=`pwd -P`
cd - >/dev/null

for bbx in *.bbox
do echo "$ThisDir"/bbox_truncate8.py -i "$bbx" -o "$bbx".csv "${args[@]:1}" && \
   "$ThisDir"/bbox_truncate8.py -i "$bbx" -o "$bbx".csv "${args[@]:1}" &&\
   "$ThisDir"/csv2ply.sh "$bbx".csv && \
   "$ThisDir"/convexHull.sh "$bbx".ply # && \
   # assimp export "$bbx".stl "$bbx".gltf
done
