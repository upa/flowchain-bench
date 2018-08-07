#!/usr/bin/env python3

# install time means, FIB is changed

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

    return


def main() :

    # open unix domain socket for controlling fc process
    p = Popen(["nc", "-uU", "/tmp/fc.sock"], bufsize = 0, stdin = PIPE)
    
    gap = 10
    for n in range (0, 1000 + gap, gap) :

        for x in range(gap) :
            install_numbered_flow(p.stdin, n + x)
        time.sleep(10)

        send_fc_cmd(p.stdin,
                    "ECHO Install MSMT Flow with %d flows installed\n" %
                    (n + gap))

        install_msmt_flow(p.stdin)
        time.sleep(10)
        send_fc_cmd(p.stdin, "ECHO Uninstall MSMT Flow")
        uninstall_msmt_flow(p.stdin)
        time.sleep(10)

    p.terminate()





if __name__ == "__main__" :

    main()
