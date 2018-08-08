#!/usr/bin/env python3

import sys

import telemetry_top_pb2
import logical_port_pb2
import base64
import json
from pprint import pprint


f = open(sys.argv[1], "rb")

nt = telemetry_top_pb2.TelemetryStream()


nt.ParseFromString(f.read())
f.close()



intfs = nt.enterprise.Extensions[telemetry_top_pb2.juniperNetworks].Extensions[logical_port_pb2.jnprLogicalInterfaceExt]

for port in intfs.interface_info :
    print(port)



