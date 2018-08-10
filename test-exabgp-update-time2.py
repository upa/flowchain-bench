#!/usr/bin/env python3

import os
import time
import math
import socket
import signal
import psutil
from subprocess import Popen, PIPE

from optparse import OptionParser


ctl_socket = None

def send_fc_cmd(cmd) :

    global ctl_socket

    print(cmd)
    ctl_socket.send(cmd.encode())
    ret = ctl_socket.recv(129)



def install_numbered_flow(flownum) :

    o3 = math.floor(flownum / 255)
    o4 = flownum % 255

    prefix = "45.1.%d.%d/32" % (math.floor(flownum / 255), flownum % 255)

    fc_cmd = "/add/%s/none/none/user-global/fp1-fn1" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(ctl_cmd)

    return

def install_bulk_flow(num) :
    ctl_cmd = "BULK %d" % num
    send_fc_cmd(ctl_cmd)
    return

def install_msmt_flow() :
    prefix = "45.0.80.1/32"
    fc_cmd = "/add/%s/none/none/user-global/fp1-fn1" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(ctl_cmd)

    return

def uninstall_msmt_flow() :
    prefix = "45.0.80.1/32"
    fc_cmd = "/delete/%s" % prefix
    ctl_cmd = "GET %s\n" % fc_cmd

    send_fc_cmd(ctl_cmd)

    return


def destroy_flow() :
    fc_cmd = "/destroy"
    ctl_cmd = "GET %s\n" % fc_cmd
    send_fc_cmd(ctl_cmd)

    return



def main() :

    # open unix domain socket for controlling fc process
    global ctl_socket
    ctl_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    ctl_socket.connect("/tmp/fc.sock")
    
    for n in range(0, 110, 10) :
        
        if n == 0 :
            x = 1
        else :
            x = n

        for y in range(30) :

            p = Popen(["/usr/local/bin/exabgp",
                       "/home/upa/work/flowchain/exabgp.conf"])
            time.sleep(10)


            send_fc_cmd("ECHO Install BULK %d Flows\n" % x)
            install_bulk_flow(x)
            time.sleep(10)

            os.kill(p.pid, signal.SIGINT)
            for p in psutil.process_iter() :
                d = p.as_dict(attrs=["pid", "cmdline"])
                if "/home/upa/work/flowchain/flowchain.py" in d["cmdline"] :
                    print("flowchain exist!! kill!!")
                    os.kill(d["pid"], signal.SIGINT)

            time.sleep(3)

if __name__ == "__main__" :

    main()
