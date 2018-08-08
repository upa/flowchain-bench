#!/usr/bin/env python3


import re
import sys
from pprint import pprint

def parse(f) :

    ifstats = {} # { ts: { "ge-1/1/1.201": bps, "ge-1/1/1.202": bps} }

    for line in f:
        s = line.split(" ")
        ts = int(s[0])
        bps = int(s[2])
        ifname = s[1][:len(s[1]) - 1]

        if not ts in ifstats :
            ifstats[ts] = {}
        
        ifstats[ts][ifname] = bps


    for ts in sorted(ifstats.keys()) :
        print("%d\t%d\t%d\t%d" % (ts,
                                  ifstats[ts]["ge-1/1/1.201"],
                                  ifstats[ts]["ge-1/1/1.202"],
                                  ifstats[ts]["ge-1/1/1.203"]
        ))

if __name__ == "__main__" :

    with open(sys.argv[1], "r") as f:
        print("#Time\t#201\t#202\t#203")
        parse(f)
