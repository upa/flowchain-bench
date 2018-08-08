#!/usr/bin/env python3



import sys



def parse(fo, over) :

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
            chain_installed = int(line.split(" ")[0].split("=")[1])
            f = False
            a = False

            if not over or flow_num > over :
                print("%d\t%d" % (flow_num, chain_installed - chain_added))
        



if __name__ == "__main__" :

    with open(sys.argv[1], "r") as f :
        print("#ChainNum\tElapsedTime")
        parse(f, None)
    
    if len(sys.argv) > 2 :
        with open(sys.argv[2], "r") as f :
            parse(f, 990)
