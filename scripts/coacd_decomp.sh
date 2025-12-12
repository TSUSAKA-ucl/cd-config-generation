#!/bin/bash
x=`readlink "$0"`
if [ $? -eq 0 ]
then cd `dirname "$x"`
else cd `dirname "$0"`
fi
ThisDir=`pwd -P`
cd - >/dev/null

if [ "$MeshlabServer" = "" ]
then MeshlabServer=meshlabserver
fi
if [ "$CoACDMain" = "" ]
then CoACDMain="$ThisDir"/../../CoACD/build/main
fi
if [ "$Blender" = "" ]
then Blender=~/Downloads/blender-3.6.23-linux-x64/blender
fi

[ $# -lt 1 ] && echo usage: "$0" "decimate_dir ..." 1>&2 && exit 1
while [ $# -ge 1 ]
do  cd "$1"
   "$MeshlabServer" -i step03_decimated.stl -o step03_decimated.obj
   "$CoACDMain" --no-merge -i step03_decimated.obj  -o step03_decimated.wrl ||\
   exit $?
   "$Blender" -b -P "$ThisDir"/split_CoACD_wrl.py
   cd -
   shift
done
