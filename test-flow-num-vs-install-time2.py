#!/usr/bin/env python3

# install time means, FIB is changed

import os
import sys
import time
import math
import signal
from subprocess import Popen, PIPE

from optparse import OptionParser


def send_fc_cmd(pipe, cmd) :

    print(cmd)
    pipe.write(cmd.encode())
    time.sleep(0.001)



def install_numbered_flow(pipe, flownum, fn_num) :

    o3 = math.floor(flownum / 255)
    o4 = flownum % 255

    prefix = "45.1.%d.%d/32" % (math.floor(flownum / 255), flownum % 255)

    chain = []
    for x in range(1, fn_num + 1) :
        chain.append("fp1-fn%d" % x)
    chain_str = "_".join(chain)

    fc_cmd = "/add/%s/none/none/user-global/%s" % (prefix, chain_str)
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(pipe, ctl_cmd)

    return

def install_msmt_flow(pipe, fn_num) :
    prefix = "45.0.80.1/32"

    chain = []
    for x in range(1, fn_num + 1) :
        chain.append("fp1-fn%d" % x)
    chain_str = "_".join(chain)

    fc_cmd = "/add/%s/none/none/user-global/%s" % (prefix, chain_str)
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(pipe, ctl_cmd)

    return

def install_bulk_flow(pipe, num) :
    ctl_cmd = "BULK %d" % num
    send_fc_cmd(pipe, ctl_cmd)
    return

def destroy_flow(pipe) :
    fc_cmd = "/destroy"
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(pipe, ctl_cmd)

    return

def uninstall_msmt_flow(pipe) :
    prefix = "45.0.80.1/32"
    fc_cmd = "/delete/%s" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(pipe, ctl_cmd)

    return


interval = 20

def main() :

    # open unix domain socket for controlling fc process
    p = Popen(["nc", "-uU", "/tmp/fc.sock"], bufsize = 0, stdin = PIPE)
    
    if len(sys.argv) > 1 :
        fn_num = int(sys.argv[1])
    else :
        fn_num = 1

    gap = 10
    for n in range (500, 1000 + gap, gap) :

        pid = Popen(["exabgp", "/home/upa/work/flowchain/exabgp.conf"]).pid
        time.sleep(5)

        send_fc_cmd(p.stdin, "ECHO ReInstall Bulk %d Flow\n" % n)
        install_bulk_flow(p.stdin, n)
        time.sleep(interval * 2)

        send_fc_cmd(p.stdin,
                    "ECHO Install MSMT Flow with %d flows installed\n" % n)

        install_msmt_flow(p.stdin, fn_num)
        time.sleep(interval)

        os.kill(pid, signal.SIGKILL)
        os.kill(pid, signal.SIGKILL)
        time.sleep(5)


    p.terminate()





if __name__ == "__main__" :

    main()
