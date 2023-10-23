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

for file in $FILES; do
    NOSOL=1 pdflatex -halt-on-error -interaction=nonstopmode $file
done

rename 's/e/exercises-/' *.pdf
mv *.pdf ../pdf
