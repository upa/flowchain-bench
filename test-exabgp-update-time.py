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

def install_bulk_flow(pipe, num) :
    ctl_cmd = "BULK %d" % num
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


def destroy_flow(pipe) :
    fc_cmd = "/destroy"
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(pipe, ctl_cmd)

    return



def main() :

    # open unix domain socket for controlling fc process
    p = Popen(["nc", "-uU", "/tmp/fc.sock"], bufsize = 0, stdin = PIPE)
    
    for n in range(1, 180, 10) :
        
        if n == 1 :
            x = 1
        else :
            x = n - 1

        send_fc_cmd(p.stdin, "ECHO Install BULK %d Flows\n" % x)
        install_bulk_flow(p.stdin, x)
        time.sleep(8)

        send_fc_cmd(p.stdin, "ECHO Destroy BULK %d Flows\n" % x)
        destroy_flow(p.stdin)
        time.sleep(8)

    p.terminate()





if __name__ == "__main__" :

    main()
