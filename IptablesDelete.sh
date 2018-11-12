#!/bin/bash

#CZYSZCZENIE STARYCH REGUŁ
iptables -F
iptables -X
iptables -F -t nat
iptables -X -t nat
iptables -F -t filter
iptables -X -t filter

# USTAWIENIE POLITYKI DZIAŁANIA
iptables -P INPUT ACCEPT
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -i lo -j ACCEPT
