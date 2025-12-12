#!/bin/bash
OutFile=`echo "$1"|sed -e 's/\.[pP][lL][yY]$/.stl/;t;d'`
[ "$OutFile" = "" ] && echo Error in "$1". 1>&2 && exit 1
docker run -u `id -u`:`id -g` -it --rm \
        -v `pwd`:/data \
	ubuntu:blender-3-6 \
	--python /opt/blender_convex_hull.py -- "$1" "$OutFile"
