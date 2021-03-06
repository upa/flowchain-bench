#!/usr/bin/env python3



import sys



def parse(fo, over, specified_ttl) :

    f = None
    a = None

    for line in fo :

        if "Install MSMT Flow" in line :
            flow_num = int(line.split(" ")[6])
            f = True
            continue

        if f and "/add/45.0.80.1/32/" in line :
            chain_added = int(line.split(" ")[2].split("=")[1])
            a = True
            continue

        if a :
            ttl = int(line.split(" ")[1].split("=")[1])
            if specified_ttl and ttl != specified_ttl :
                continue

            chain_installed = int(line.split(" ")[0].split("=")[1])
            f = False
            a = False

            if not over or flow_num > over :
                print("%d\t%d" % (flow_num, chain_installed - chain_added))
        



if __name__ == "__main__" :

    if len(sys.argv) > 2 :
        ttl = int(sys.argv[2])
    else :
        ttl = None

    with open(sys.argv[1], "r") as f :
        print("#ChainNum\tElapsedTime")
        parse(f, None, ttl)
    
