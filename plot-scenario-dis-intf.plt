set terminal pdf enhanced color fontscale 0.8
set output "graph/graph-dis-intf.pdf"

set ylabel "throughput (Mbps)"
set xlabel "time (sec)"

set size ratio 0.4

set xrange [0:76]
set yrange [-100:1100]

unset grid
set key at 75,800


plot	"dat/dis-intf.txt" using ($0*2):($2/1000000) \
	with lp ps 0.8 title "Fn link",	\
	"dat/dis-intf.txt" using ($0*2):($3/1000000) \
	with lp ps 0.8 title "Backup link"
