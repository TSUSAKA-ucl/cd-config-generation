#!/bin/bash
Links=(`for ff in "$@"
do echo "$ff" | sed 's/\(_[0-9]*\)\?\.bbox\.ply$//'
done | sort -u`)
echo '['
INDENT='  '
HDR="$INDENT"'['
for link in "${Links[@]}"
do Parts=(`ls "$link"*.bbox.ply`)
   for pp in "${Parts[@]}"
   do echo -n "$HDR" '"'"$pp"'"'
      HDR=', '
   done
   echo -n ']'
   HDR=',
'"$INDENT"'['
done
echo
echo ']'
exit 0
