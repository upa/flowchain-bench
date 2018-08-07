#!/usr/bin/env python3

import re
import sys

def parse(f) :
    
    for line in f:
        if re.search(r"BULK=\d+", line):
            bulk = int(line.split(" ")[1].split("=")[1])
            diff = int(line.split(" ")[4].split("=")[1])
            print("%d\t%d" % (bulk, diff))


if __name__ == "__main__" :

    with open(sys.argv[1], "r") as f:
        print("#BulkNum\tTime")
        parse(f)
