#!/bin/bash
x=`readlink "$0"`
if [ $? -eq 0 ]
then cd `dirname "$x"`
else cd `dirname "$0"`
fi
ThisDir=`pwd -P`
cd -

for stlIn in `ls -1 *.[Ss][Tt][Ll] |grep -v '\.bbox'`
do OutFile=`echo "$stlIn"|sed -e 's/\.[a-zA-Z]\+$/.bbox/;t;d'`
   if [ -f "$OutFile" ]
   then echo "$OutFile" exists. skip creation 1>&2
   else "$ThisDir"/boundingBox.sh "$stlIn"
   fi
done
