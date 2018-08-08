set terminal pdf enhanced color fontscale 0.7
set output "graph/graph-add-fn.pdf"

set ylabel "throughput (Mbps)"
set xlabel "time (sec)"

set size ratio 0.3

set yrange [-20:160]
set ytic 0,20
set xrange [0:80]
set xtic 5

unset grid
set key at 79,100

set parametric
set trange[-20:160]
afn1=11
afn2=21
afn3=32
rfn1=42
rfn2=53
rfn3=63
ly=148

set label 1 "Add\nFn1" at afn1+0.5,ly
set label 2 "Add\nFn2" at afn2+0.5,ly
set label 3 "Add\nFn3" at afn3+0.5,ly
set label 4 "Remove\nFn1" at rfn1+0.5,ly
set label 5 "Remove\nFn2" at rfn2+0.5,ly
set label 6 "Remove\nFn3" at rfn3+0.5,ly

plot	"dat/add-fn-ifstat.txt" using ($0*2):($2/1000000) \
	with l title "Fn1",	\
	"dat/add-fn-ifstat.txt" using ($0*2):($3/1000000) \
	with l title "Fn2",	\
	"dat/add-fn-ifstat.txt" using ($0*2):($4/1000000) \
	with l title "Fn3",	\
	afn1,t with l lt 1 lc rgb "gray40" lw 1 notitle,	\
	afn2,t with l lt 1 lc rgb "gray40" lw 1 notitle,	\
	afn3,t with l lt 1 lc rgb "gray40" lw 1 notitle,	\
	rfn1,t with l lt 1 lc rgb "gray40" lw 1 notitle,	\
	rfn2,t with l lt 1 lc rgb "gray40" lw 1 notitle,	\
	rfn3,t with l lt 1 lc rgb "gray40" lw 1 notitle	

