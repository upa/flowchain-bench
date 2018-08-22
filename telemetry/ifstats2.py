#!/usr/bin/env python3

import sys
import socket
from contextlib import closing

import time
import telemetry_top_pb2 as tl_pb2
import logical_port_pb2 as lp_pb2

from optparse import OptionParser


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def gather_telemetry(sock, port_names, direct) :

    hosts = {}
    #ifstats = {} # ifname: [ (ts, octs_before), (ts, octs_after) ]

    with closing(sock) :

        while True:
            msg = sock.recv(40960)
            tl = tl_pb2.TelemetryStream()
            tl.ParseFromString(msg)

            ts = tl.timestamp / 1000

            system = tl.system_id
            if not system in hosts :
                hosts[system] = {}

            ifstats = hosts[system]
            jnpr_ext = tl.enterprise.Extensions[tl_pb2.juniperNetworks]
            ports = jnpr_ext.Extensions[lp_pb2.jnprLogicalInterfaceExt]

            for port in ports.interface_info :

                if not port.if_name in port_names :
                    continue

                if not port.if_name in ifstats :
                    if direct == "egress" :
                        octet = port.egress_stats.if_octets
                    else :
                        octet = port.ingress_stats.if_octets
                    ifstats[port.if_name] = [(ts, octet), (ts, octet)]
                    continue
                
                x = ifstats[port.if_name]
                x.pop(0)

                if direct == "egress" :
                    x.append((ts, port.egress_stats.if_octets))
                else :
                    x.append((ts, port.ingress_stats.if_octets))
                
                bit_diff = (x[1][1] - x[0][1]) * 8
                ts_diff = (x[1][0] - x[0][0])
                print("%d %s %s: %d bps" %
                      (time.time(), system, port.if_name, bit_diff / ts_diff),
                      flush = True)


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
    parser.add_option(
        "-d", "--direction", type = "choice",
        choices = [ "ingress", "egress" ], default = "ingress",
        dest = "direction",
        help = "direction of traffic"
    )

    (option, args) = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((option.addr, option.port))

    gather_telemetry(sock, option.port_names, option.direction)
