set terminal pdf enhanced color fontscale 1
set output "graph/graph-dis-interfp.pdf"

set ylabel "throughput (Mbps)"
set xlabel "time (sec)"

set size ratio 0.3

set xrange [0:66]
set yrange [-100:1100]

unset grid
set key at 34,800


plot	"dat/dis-interfp-mx5-1-401.dat" using ($0*2):($2/1000000) \
	with lp ps 0.8 title "MX5-1 to MX5-2", \
	"dat/dis-interfp-mx5-2-101.dat" using ($0*2):($2/1000000) \
	with lp ps 0.8 title "MX5-2 to ns-ext", \
	"dat/dis-interfp-mx5-1-100.dat" using ($0*2):($2/1000000) \
	with lp ps 0.8 title "MX5-1 to ns-ext",	\
