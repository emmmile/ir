set terminal svg enhanced size 800 500 fname "Times" fsize 12 dashed
#set output "statistics.svg"


set key left nobox
#set samples 1000
set xlabel "Number of nodes"
set ylabel "Time per assignament [µs]"
plot 'file.plot' using xcoord(1):2 smooth csplines title 'ptree' with lines
