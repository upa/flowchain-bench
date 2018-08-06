set terminal pdf enhanced color fontscale 1
set output "graph/graph-flow-num-vs-install-time.pdf"

set ylabel "install time (msec)"
set xlabel "number of installed chains"

set size ratio 0.4

set yrange [0:]
set xrange [0:1000]

set key bottom


plot	"dat/flow-num-vs-install.dat" using 1:($2/1000) with l notitle
