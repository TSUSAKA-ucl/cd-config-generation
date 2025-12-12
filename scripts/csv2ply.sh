#!/usr/bin/bash
while [ $# -gt 0 ]
do plyFile=`echo "$1"|sed -e 's/\.[a-zA-Z0-9]\+$/.ply/'`
   lines=`cat "$1"|wc -l`
   echo "$plyFile"
   # sed -e 's/\(,[ \t]*[0-9\.]\+[ \t]*,[ \t]*[0-9\.]\+[ \t]*\),[ \t]*[0-9\.]\+[ \t]*$/\1/' 
   sed -e 's/,1$//' \
       -e 's/,/ /g' \
       -e '1iply\
format ascii 1.0\
element vertex '$lines'\
property float x\
property float y\
property float z\
end_header' "$1" > "$plyFile"
   shift
done
