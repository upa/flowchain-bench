#!/usr/bin/env python3

import os
import re
import sys
import statistics

def parse(f) :

    res = {} # { flownum: [diff, diff, diff, ... ] }
    flownum = 0

    for line in f :
        if re.match(r"TS=\d+ TTL=\d+ DIFF=\d+", line) :
            diff = int(line.split(" ")[2].split("=")[1])
            if not flownum in res :
                res[flownum] = []
            res[flownum].append(diff)

        elif "ECHO Install MSMT Flow with" in line :
            flownum = int(line.split(" ")[6])


    for k in sorted(res.keys()) :
        print("%d\t%f\t%f\t%d\t%d\t%f" % (k,
                                          statistics.mean(res[k]),
                                          statistics.median(res[k]),
                                          min(res[k]),
                                          max(res[k]),
                                          statistics.pstdev(res[k])
        ))


if __name__ == "__main__" :

    with open(sys.argv[1], "r") as f :
        print("#Flownum\tAvg\tMid\tMin\tMax\tStdEv")
        parse(f)


