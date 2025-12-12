#!/bin/bash
BBOX_MLX=`mktemp`
cat >"$BBOX_MLX" <<EOF
<!DOCTYPE FilterScript>
<FilterScript>
  <filter name="Compute Geometric Measures"/>
</FilterScript>
EOF
[ $# -lt 1 ] && echo "usage:$0 file" 1>&2 && exit 1
while [ $# -ge 1 ]
do  OutFile=`echo "$1"|sed -e 's/\.[a-zA-Z]\+$/.bbox/;t;d'`
    [ "$OutFile" = "" ] && echo Error in "$1". 1>&2 && exit 1
    meshlabserver -i "$1" -o /dev/null -s "$BBOX_MLX" 2>&1 | \
	grep '^Mesh ' > "$OutFile"
    shift
done
rm "$BBOX_MLX"
