#!/bin/bash
# 引数のSTLファイル毎に、STLから頂点だけ抜き出してconvex hullを求めてその頂点をplyに保存
[ "$ScriptDir" = "" ] && ScriptDir=~/Test/gjk_worker/scripts
while [ $# -gt 0 ]
do Ply=`basename "${1%.*}".ply`
   echo "$1" to "$Ply"
   rm input.stl
   [ -f  vertices.ply ] && rm  vertices.ply
   ln -s "$1" input.stl && \
	python3 "$ScriptDir"/extract-vertices-only.py &&\
	mv vertices.ply "$Ply" &&\
	"$ScriptDir"/convexHull.sh "$Ply"
   shift
done
