#!/bin/bash
# Setup network interface for SNIFFER
# MUST BE RUN AS ROOT!
ip link set eth0 down
ip addr add 192.168.100.3/24 brd 192.168.100.255 dev eth0
ip link set eth0 up
ip route add default via 192.168.100.1
#uncomment to add full network access via DNS
#echo "nameserver 192.168.100.1" | sudo tee /etc/resolv.conf

# look at traffic inflow on 5005 with netcat
# nc -lu -p 5005
# better yet, look at it with tcpdump
#sudo tcpdump -i eth0 udp port 5005 -vv