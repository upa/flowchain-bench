#!/usr/bin/env python3

import sys
import socket
from contextlib import closing

import telemetry_top_pb2
import logical_port_pb2
from pprint import pprint



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ifstats = {} # ifname: [ octs_before, octs_after ]

with closing(sock) :
    sock.bind(("45.0.70.10", 30000))

    seq = 0
    while True:

        msg = sock.recv(40960)
        nt = telemetry_top_pb2.TelemetryStream()
        nt.ParseFromString(msg)

        jnpr_ext = nt.enterprise.Extensions[telemetry_top_pb2.juniperNetworks]
        ports = jnpr_ext.Extensions[logical_port_pb2.jnprLogicalInterfaceExt]

        for port in ports.interface_info :

            if not "ge-1/1/1.20" in port.if_name :
                continue

            if not port.if_name in ifstats :
                ifstats[port.if_name] = [ 0, 0 ]
                
            x = ifstats[port.if_name]

            x.pop(0)
            x.append(port.ingress_stats.if_octets)

            print("%s: %d bps" % (port.if_name, (x[1] - x[0]) * 8))

