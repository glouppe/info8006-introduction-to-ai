#!/bin/bash

#XXX : Do not use or modify. See submission_test.sh

#Install Python 3 and flake8
#sudo yum -y update &> /dev/null
#sudo yum -y install python3 flake8 &> /dev/null

source ./vars

#Class name of agent should be named $f$ with first-letter capitalized
srcname=`echo $src | sed 's/\.py//g'| sed 's/\///' | sed 's/.//'`
srcname="${srcname^}"

c=`cat $src | grep -c "class $srcname"`
if [ $c -ne 1 ]; then
        echo "There is no unique agent class matching file name with first capitalized letter. Please resubmit following the rules."
        exit -1
fi
        

#A move method should be defined
c=`cat $src | grep -c "def move(self*"`
if [ $c -lt 1 ]; then
        echo "There is no move function inside the file. Please resubmit following the rules."
        exit -1
fi

#An init method should be defined
c=`cat $src | grep -c "def __init__(self*"`
if [ $c -lt 1 ]; then
        echo "There is no init function inside the file. Please resubmit following the rules."
        exit -1
fi



#There shouldn't be any syntax error in the file
python3 -m py_compile $src 2> err_file
err=`cat err_file`
if [ -n "$err" ]; then
        echo "It seems there is an error in your file, you should check it. Please find below your error : "
        echo $err
        exit -1
fi

echo "Agent file seems valid. However, this script cannot verify everything. Be sure the specifications of the class meet the requirements described in the project assignment."

echo "srcname=\"$srcname\"" >> ./vars

