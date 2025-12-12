#!/bin/bash
HDR='[
'
for ff in "$@"
do echo -n "$HDR"'  [ "'"$ff"'" ]'
   HDR=',
'
done
echo '
]'
