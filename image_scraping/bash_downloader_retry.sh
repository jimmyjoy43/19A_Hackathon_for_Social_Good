#!/bin/bash

id=$1
url=$2
urlid=`basename $url`

if [ -s $id ]
then
 :
else
 wget -c $url -O $id
fi
