#!/bin/bash

id=$1
url=$2
urlid=`basename $url`
wget -c $url -O $id




