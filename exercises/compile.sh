#!/bin/bash
# Build the exercise sheets into ../pdf, with and without solutions.
#
#   ./compile.sh            # every sheet
#   ./compile.sh e3.tex     # one sheet
#
# eN.tex gives ../pdf/exercises-N-solutions.pdf and, with \NOSOL defined, the
# student version ../pdf/exercises-N.pdf. Auxiliary files go to build/.

set -euo pipefail
cd "$(dirname "$0")"

if (($# > 0)); then
    files=("$@")
else
    files=(e[0-9]*.tex)
fi

mkdir -p build
for file in "${files[@]}"; do
    sheet=$(basename "$file" .tex)
    n=${sheet#e}
    for variant in solutions student; do
        if [[ $variant == solutions ]]; then
            job="exercises-$n-solutions"
            input="\\input{$sheet.tex}"
        else
            job="exercises-$n"
            input="\\def\\NOSOL{}\\input{$sheet.tex}"
        fi
        for pass in 1 2; do
            if ! pdflatex -halt-on-error -interaction=nonstopmode -output-directory=build \
                    -jobname="$job" "$input" > /dev/null; then
                echo "error: $job did not compile, see build/$job.log" >&2
                exit 1
            fi
        done
        mv "build/$job.pdf" "../pdf/$job.pdf"
        echo "../pdf/$job.pdf"
    done
done
