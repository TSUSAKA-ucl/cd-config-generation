#!/bin/bash
x=`readlink "$0"`
if [ $? -eq 0 ]
then cd `dirname "$x"`
else cd `dirname "$0"`
fi
ThisDir=`pwd -P`
cd -
args=("$@")
echo "$ThisDir"/bbox_truncate8.py -i "$1" -o "$1".csv "${args[@]:1}"
"$ThisDir"/bbox_truncate8.py -i "$1" -o "$1".csv "${args[@]:1}"
"$ThisDir"/csv2ply.sh "$1".csv
"$ThisDir"/convexHull.sh "$1".ply
assimp export "$1".stl "$1".gltf
