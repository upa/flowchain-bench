#!/bin/bash

./parser-flow-num-vs-install-time.py \
	output/flow-num-vs-install_chain-1_2.txt	\
	> dat/flow-num-vs-install_chain-1.dat

./parser-flow-num-vs-install-time.py \
	output/flow-num-vs-install_chain-5_2.txt	\
	> dat/flow-num-vs-install_chain-5.dat

./parser-flow-num-vs-install-time.py \
	output/flow-num-vs-install_chain-10_2.txt	\
	> dat/flow-num-vs-install_chain-10.dat

./parser-chain-num-vs-delay.py \
	output/chain-num-vs-deley.txt \
	> dat/chain-num-vs-delay.dat

./parser-exabgp-update-time.py \
	output/exabgp-update-time_3.txt \
	> dat/exabgp-update-time.dat


./parser-scenario-add-fn.py \
	output/scenario-add-fn-ifstat.txt \
	> dat/add-fn-ifstat.txt

./parser-scenario-dis-intf.py \
	output/scenario-dis-intf.txt \
	> dat/dis-intf.txt
