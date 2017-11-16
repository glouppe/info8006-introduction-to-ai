#!/bin/bash

#XXX : Do not use or modify. See submission_test.sh

#Get the list of files in the tar.gz
filelist=$(tar -ztf "$1")
#Error?
if [ $? -ne 0 ]; then
 echo "ERROR ! Unknown archive type ! Is it compressed in gz?"
 echo "Filename : $(basename $1)"
 exit -1
fi

#Empty?
if [ -z "$filelist" ]; then
 echo "ERROR ! Archive seems empty ! Check archive type... It must be a .tar.gz."
 exit -1
fi

#agent%id.py not found ?
tar zxf $1
f=`find . -name 'agent[0-9][0-9][0-9][0-9][0-9][0-9].py'`
if [ -z "$f" ]; then
        echo "Main agent file not found. Check that your agent follows this pattern : agent%id.py where %id is your student number without 's'"
        exit -1
fi

#Several agent%id.py found ?
nbf=`echo $f | wc -w` 

if [ $nbf -gt 1 ]; then
        echo "Several files with same pattern as the main agent file. Check the unicity of your main agent filename pattern"
        exit -1
fi

echo "Your main agent file is $f. If it is not the case, resubmit following the rules !"

echo "src=\"$f\"" > ./vars
