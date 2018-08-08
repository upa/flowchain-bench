#!/usr/bin/env python3

import sys
import socket
from contextlib import closing

import time
import telemetry_top_pb2 as tl_pb2
import logical_port_pb2 as lp_pb2

from optparse import OptionParser


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def gather_telemetry(sock, port_names) :

    ifstats = {} # ifname: [ octs_before, octs_after ]

    with closing(sock) :

        while True:
            msg = sock.recv(40960)
            tl = tl_pb2.TelemetryStream()
            tl.ParseFromString(msg)

            jnpr_ext = tl.enterprise.Extensions[tl_pb2.juniperNetworks]
            ports = jnpr_ext.Extensions[lp_pb2.jnprLogicalInterfaceExt]

            for port in ports.interface_info :

                if not port.if_name in port_names :
                    continue

                if not port.if_name in ifstats :
                    ifstats[port.if_name] = [ 0, 0 ]
                
                x = ifstats[port.if_name]
                x.pop(0)
                x.append(port.ingress_stats.if_octets)
                print("%d %s: %d bps" %
                      (time.time(), port.if_name, (x[1] - x[0]) * 8))


if __name__ == "__main__" :

    desc = "usage: %prog [options]"
    parser = OptionParser(desc)

    parser.add_option(
        "-p", "--port", type = "int", default = 30000, dest = "port",
        help = "Listen port for receiving telemetry"
    )
    parser.add_option(
        "-b", "--bind-addr", type = "string", default = "0.0.0.0",
        dest = "addr",
        help = "Bind address for receivng telemetry"
    )
    parser.add_option(
        "-i", "--interface", type = "string", action = "append",
        dest = "port_names",
        help = "interface name stats gathered"
    )


    (option, args) = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((option.addr, option.port))

    gather_telemetry(sock, option.port_names)
