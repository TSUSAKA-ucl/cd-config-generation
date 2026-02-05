#!/bin/bash
if [[ "$VIRTUAL_ENV" = "" ]]; then
    echo "Please activate your Python virtual environment first." 1>&2
    exit 1
fi
if pip show pymeshlab > /dev/null 2>&1; then
    :
else
    echo 'Please install "pymeshlab" in your Python virtual environment first.' 1>&2
    exit 1
fi
# -sオプションでスケールを指定可能にする
Scale=1.0
while getopts s: opt
do  case $opt in
	s)  Scale=$OPTARG
	    ;;
	\?) echo "usage:$0 [-s scale] file1 [file2 ...]" 1>&2
	    exit 1
	    ;;
    esac
done
shift `expr $OPTIND - 1`

[ $# -lt 1 ] && echo "usage:$0 file" 1>&2 && exit 1
while [ $# -ge 1 ]
do  OutFile=`echo "$1"|sed -e 's/\.[a-zA-Z]\+$//;t;d'`
    [ "$OutFile" = "" ] && echo Error in "$1". 1>&2 && exit 1
    echo "Processing file $1 ..."
    python3 << EOF  > "$OutFile".bbox
import pymeshlab
ms = pymeshlab.MeshSet()
ms.load_new_mesh('$1')
ms.apply_filter('compute_matrix_from_scaling_or_normalization',
                 axisx=$Scale, axisy=$Scale, axisz=$Scale,
                 uniformflag=True)
ms.apply_filter('apply_matrix_freeze')
m = ms.current_mesh()
bbox = m.bounding_box()
print(f"Mesh ${1} after scaling $Scale:")
print(f"Mesh Bounding Box Size {bbox.dim_x():.6f} {bbox.dim_y():.6f} {bbox.dim_z():.6f}")
print(f"Mesh Bounding Box Diag {bbox.diagonal():.6f}")
print(f"Mesh Bounding Box min {bbox.min()[0]:.6f} {bbox.min()[1]:.6f} {bbox.min()[2]:.6f}")
print(f"Mesh Bounding Box max {bbox.max()[0]:.6f} {bbox.max()[1]:.6f} {bbox.max()[2]:.6f}")
# さらにscaleしたメッシュをPLY形式で保存
ms.save_current_mesh('$OutFile'+'.ply', binary=False)
EOF
    shift
done
