#!/usr/bin/env python3

import time
import math
from subprocess import Popen, PIPE

from optparse import OptionParser


def send_fc_cmd(pipe, cmd) :

    print(cmd)
    pipe.write(cmd.encode())
    time.sleep(0.001)



def install_numbered_flow(pipe, flownum) :

    o3 = math.floor(flownum / 255)
    o4 = flownum % 255

    prefix = "45.1.%d.%d/32" % (math.floor(flownum / 255), flownum % 255)

    fc_cmd = "/add/%s/none/none/user-global/fp1-fn1" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(pipe, ctl_cmd)

    return

def install_msmt_flow(pipe) :
    prefix = "45.0.80.1/32"
    fc_cmd = "/add/%s/none/none/user-global/fp1-fn1" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(pipe, ctl_cmd)

    return

def uninstall_msmt_flow(pipe) :
    prefix = "45.0.80.1/32"
    fc_cmd = "/delete/%s" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(pipe, ctl_cmd)

def override_msmt_flow(pipe, chain) :
    prefix = "45.0.80.1/32"
    fc_cmd = "/override/%s/none/none/user-global/%s" % (prefix, chain)
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(pipe, ctl_cmd)

    return


def main() :

    # open unix domain socket for controlling fc process
    p = Popen(["nc", "-uU", "/tmp/fc.sock"], bufsize = 0, stdin = PIPE)
    
    fns = []
    for n in range(1, 33) :
        fns.append("fp1-fn%d" % n)
        chain = "_".join(fns)
        
        send_fc_cmd(p.stdin,
                    "ECHO Install MSMT Flow with %d of Functions\n" % n)

        override_msmt_flow(p.stdin, chain)
        time.sleep(20)
        
    p.terminate()





if __name__ == "__main__" :

    main()
