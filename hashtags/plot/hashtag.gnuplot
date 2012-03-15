set terminal svg enhanced size 800 500 fname "Times" fsize 12 dashed
set output "plot.svg"

set xlabel "Hashtags (sorted on score)"
set ylabel "Score (sum of rhos)"
plot '1000.plot' using 1:2 smooth csplines title 'hashtags score' with lines
