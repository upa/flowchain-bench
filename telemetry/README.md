
### Gathering interface statistics using telemetry from Juniper MX

0. Configure your MX devices https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/junos-telemetry-interface-configuring.html
1. Download JUNOS Telemetry Interface Data Model Files from https://www.juniper.net/support/downloads/?p=mx240
2. Compile logical_port.proto and telemetry_top.proto using `protoc`.
3. ./ifstats.py -i ge-1/1/1.201 -i ge-1/1/1.801
