set terminal pdf enhanced color fontscale 0.9
set output "graph/graph-exabgp-update-time.pdf"

set ylabel "time (msec)"
set xlabel "number of installed chains"

set size ratio 0.4

set yrange [0:]
set xrange [0:170]

set xtic 10

plot	"dat/exabgp-update-time.dat" using 1:($2/1000) with lp notitle
