#!/usr/bin/env bash

#XXX : Do not use or modify. See submission_test.sh

flkout="`flake8 *.py`"
#File should pass flake8 style
if [ -n "$flkout" ]; then
        echo "Source code style does not meet flake8 standards. Please ensure it does using flake8, you can use autopep8 to automatize a part of the work for you."
        echo "Usage of autopep8 : autopep8 --in-place --aggressive --aggressive yourfile.py"
        exit -1
fi
echo "Source code passed flake8 style !"
