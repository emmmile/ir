#/bin/bash

pdflatex -shell-escape hashtag.tex
rm hashtag-figure0.d* *.log *.aux* hashtag.pdf
mv hashtag-figure0.pdf plotFrequency.pdf