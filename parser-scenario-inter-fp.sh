#!/bin/bash

cat output/scenario-dis-inter-fp.txt \
	| grep "mx5-1:45.0.70.1 ge-1/1/0.100" | cut -d " " -f 1,4	\
	> dat/dis-interfp-mx5-1-100.dat


cat output/scenario-dis-inter-fp.txt \
	| grep "mx5-1:45.0.70.1 ge-1/1/0.401" | cut -d " " -f 1,4	\
	> dat/dis-interfp-mx5-1-401.dat

cat output/scenario-dis-inter-fp.txt \
	| grep "mx5-2:45.0.70.2 ge-1/1/0.101" | cut -d " " -f 1,4	\
	> dat/dis-interfp-mx5-2-101.dat
