#!/bin/bash
# Setup network interface for SNIFFER
# MUST BE RUN AS ROOT!
ip addr add 192.168.100.3/24 brd 192.168.100.255 dev eth0
ip link set eth0 up
ip route add default via 192.168.100.1
#uncomment to add full network access via DNS
#echo "nameserver 192.168.100.1" | sudo tee /etc/resolv.conf


