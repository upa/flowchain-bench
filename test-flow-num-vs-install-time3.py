#!/usr/bin/env python3

# install time means, FIB is changed

import os
import sys
import time
import math
import signal
import socket
from subprocess import Popen, PIPE

from optparse import OptionParser


ctl_socket = None

def send_fc_cmd(cmd) :

    global ctl_socket

    print(cmd)
    ctl_socket.send(cmd.encode())
    ret = ctl_socket.recv(128)


def install_numbered_flow(flownum, fn_num) :

    o3 = math.floor(flownum / 255)
    o4 = flownum % 255

    prefix = "45.1.%d.%d/32" % (math.floor(flownum / 255), flownum % 255)

    chain = []
    for x in range(1, fn_num + 1) :
        chain.append("fp1-fn%d" % x)
    chain_str = "_".join(chain)

    fc_cmd = "/add/%s/none/none/user-global/%s" % (prefix, chain_str)
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(ctl_cmd)

    return

def install_msmt_flow(fn_num) :
    prefix = "45.0.80.1/32"

    chain = []
    for x in range(1, fn_num + 1) :
        chain.append("fp1-fn%d" % x)
    chain_str = "_".join(chain)

    fc_cmd = "/add/%s/none/none/user-global/%s" % (prefix, chain_str)
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(ctl_cmd)

    return

def install_bulk_flow(num) :
    ctl_cmd = "BULK %d" % num
    send_fc_cmd(ctl_cmd)
    return

def destroy_flow() :
    fc_cmd = "/destroy"
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(ctl_cmd)

    return

def uninstall_msmt_flow() :
    prefix = "45.0.80.1/32"
    fc_cmd = "/delete/%s" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(ctl_cmd)

    return


interval = 15

def main() :

    global ctl_socket
    ctl_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ctl_socket.connect("/tmp/fc.sock")
    
    if len(sys.argv) > 1 :
        fn_num = int(sys.argv[1])
    else :
        fn_num = 1

    gap = 50
    start = 0

    if start > 0 :
        send_fc_cmd("ECHO Strt to Install Bulk %d Flow\n" % start)
        install_bulk_flow(start)
        print("Bulk %d done\n" % start)
        time.sleep(interval)

    for n in range (start, 1000 + gap, gap) :

        send_fc_cmd("ECHO Install MSMT Flow with %d flows installed\n" % n)
        install_msmt_flow(fn_num)
        time.sleep(interval)

        send_fc_cmd("ECHO Install more %d flows and remove msmt flow" % gap)
        for x in range(gap) :
            install_numbered_flow(n + x, fn_num)
        uninstall_msmt_flow()
        time.sleep(interval)
        

    ctl_socket.close()


if __name__ == "__main__" :

    main()
