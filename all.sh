#!/bin/bash

./parser-flow-num-vs-install-time.py \
	output/flow-num-vs-install_per-10flows_2.txt \
	output/flow-num-vs-install_per-10flows_over980.txt \
	> dat/flow-num-vs-install.dat

./parser-chain-num-vs-delay.py \
	output/chain-num-vs-deley.txt \
	> dat/chain-num-vs-delay.dat

./parser-exabgp-update-time.py \
	output/exabgp-update-time_3.txt \
	> dat/exabgp-update-time.dat


./parser-scenario-add-fn.py \
	output/scenario-add-fn-ifstat.txt \
	> dat/add-fn-ifstat.txt
