#!/bin/bash
x=`readlink "$0"`
if [ $? -eq 0 ]
then cd `dirname "$x"`
else cd `dirname "$0"`
fi
ThisDir=`pwd -P`
cd - >/dev/null
if [ "$Blender" = "" ]
then Blender=~/Downloads/blender-3.6.23-linux-x64/blender
fi

OutFile="${1%.*}.stl"
[ -e "$OutFile" ] && echo "$OutFile exists, skipping conversion." 1>&2 && exit 1
Args=`xmllint --xpath '//MLMesh[@visible="1"]/@filename' "$1" |\
	          sed -e 's/^[[:blank:]]*filename[[:blank:]]*=[[:blank:]]*\(["'"'"'].*\)$/\1/;t;d' |\
		      sed -e ':a;N;$!ba;s/\n/ /g' `
echo "Converting $Args to $OutFile" 1>&2
eval "$Blender -b -P $ThisDir/blender_convex_hull_multi.py -- $Args $OutFile" || \
    echo "Conversion failed" 1>&2 && exit 1
