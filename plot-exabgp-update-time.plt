set terminal pdf enhanced color fontscale 0.9
set output "graph/graph-exabgp-update-time.pdf"

set ylabel "time (msec)"
set xlabel "number of installing chains"

set size ratio 0.4

set yrange [0:]
set xrange [1:]

set xtic 50

plot	"dat/exabgp-update-time.dat"	\
	using 1:($2/1000):xtic(1) with l lc 1 notitle,	\
	"dat/exabgp-update-time.dat"	\
	using 1:($2/1000):($4/1000):($5/1000) \
	with yerrorbars lc 1 lt 1 notitle 

