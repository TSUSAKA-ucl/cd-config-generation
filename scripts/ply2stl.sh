#!/usr/bin/bash
script=`mktemp` || exit 1
cat >"$script" <<EOF
<!DOCTYPE FilterScript>
<FilterScript>
  <filter name="Convex Hull">
  </filter>
</FilterScript>
EOF
while [ $# -gt 0 ]
do stlFile="${1%.ply}.STL"
   meshlabserver -i "$1" -o "$stlFile" -s "$script"
   shift
done
/usr/bin/rm "$script"
