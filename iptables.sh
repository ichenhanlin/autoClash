#!/bin/sh

sudo iptables -t nat -N CLASH

sudo iptables -t nat -A CLASH -d 0.0.0.0/8 -j RETURN
sudo iptables -t nat -A CLASH -d 10.0.0.0/8 -j RETURN
sudo iptables -t nat -A CLASH -d 127.0.0.0/8 -j RETURN
sudo iptables -t nat -A CLASH -d 169.254.0.0/16 -j RETURN
sudo iptables -t nat -A CLASH -d 172.16.0.0/12 -j RETURN
sudo iptables -t nat -A CLASH -d 192.168.0.0/16 -j RETURN
sudo iptables -t nat -A CLASH -d 224.0.0.0/4 -j RETURN
sudo iptables -t nat -A CLASH -d 240.0.0.0/4 -j RETURN

sudo iptables -t nat -A CLASH -p tcp -j REDIRECT --to-ports 7892

sudo iptables -t nat -A PREROUTING -p tcp -j CLASH

sudo iptables -t nat -A OUTPUT -p tcp --dport 53 -d 8.8.8.8 -j CLASH
