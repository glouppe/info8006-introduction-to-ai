#!/bin/bash

set -e

if (($# > 0)); then
    FILES=$@
else
    FILES=*.tex
fi

for file in $FILES; do
    pdflatex -halt-on-error -interaction=nonstopmode $file
done

rename 's/e(\d)/exercises-$1-solutions/' *.pdf
mv *.pdf ../pdf

cp common.sty backup.sty
sed -i 's/\\BODY//g' common.sty

for file in $FILES; do
    pdflatex -halt-on-error -interaction=nonstopmode $file
done

rename 's/e/exercises-/' *.pdf
mv *.pdf ../pdf

mv backup.sty common.sty
