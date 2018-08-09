set terminal pdf enhanced color fontscale 1
set output "graph/graph-flow-num-vs-install-time.pdf"

set ylabel "install time (msec)"
set xlabel "number of installed chains"

set size ratio 0.4

set yrange [0:]
set xrange [0:1000]

set key at 980,3700

plot	"dat/flow-num-vs-install_chain-1.dat" \
	using 1:($2/1000) with lp title "1 Fn chains", \
	"dat/flow-num-vs-install_chain-5.dat" \
	using 1:($2/1000) with lp title "5 Fn chains",	\
	"dat/flow-num-vs-install_chain-10.dat" \
	using 1:($2/1000) with lp title "10 Fn chains"
