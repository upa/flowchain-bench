set terminal pdf enhanced color fontscale 1
set output "graph/graph-chain-num-vs-delay.pdf"

set ylabel "latency (usec)"
set xlabel "number of chained functions"

set size ratio 0.4

set yrange [0:600]
set xrange [0:32]

set key bottom


plot	"dat/chain-num-vs-delay.dat" \
	using 1:3 with l lc 1 notitle,	\
	"dat/chain-num-vs-delay.dat" \
	using 1:3:4:5 with yerrorbars lc 1 ps 0.2 notitle
