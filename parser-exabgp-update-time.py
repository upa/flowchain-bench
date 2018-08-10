#!/usr/bin/env python3

import re
import sys
import statistics as stat

def parse(f) :
    
    res = {} # { bulknum : [ diff, diff, diff ...]}

    for line in f:
        if re.search(r"BULK=\d+", line):
            bulk = int(line.split(" ")[1].split("=")[1])
            diff = int(line.split(" ")[4].split("=")[1])

            if not bulk in res :
                res[bulk] = []

            res[bulk].append(diff)

    for bulk in sorted(res.keys()) :
        print("%d\t%.2f\t%d\t%d\t%d\t%f" % (bulk,
                                          stat.mean(res[bulk]),
                                          stat.median(res[bulk]),
                                          min(res[bulk]),
                                          max(res[bulk]),
                                          stat.pstdev(res[bulk])
        ))


if __name__ == "__main__" :

    with open(sys.argv[1], "r") as f:
        print("#Bulk\tMean\tMed\tMin\tMax\tStdev")
        parse(f)
