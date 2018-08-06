#!/bin/bash

./parser-flow-num-vs-install-time.py \
	output/flow-num-vs-install_per-10flows.txt \
	> dat/flow-num-vs-install.dat


./parser-chain-num-vs-delay.py \
	output/chain-num-vs-deley.txt \
	> dat/chain-num-vs-delay.dat
