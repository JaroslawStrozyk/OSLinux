#!/bin/bash
 
### BEGIN INIT INFO
# Provides:          firewall.sh
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

# CZYSZCZENIE STARYCH REGUŁ
iptables -F
iptables -X
iptables -F -t nat
iptables -X -t nat
iptables -F -t filter
iptables -X -t filter

# USTAWIENIE POLITYKI DZIAŁANIA
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -i lo -j ACCEPT

# KASOWANIE PING-ów
# iptables -A INPUT -p icmp --icmp-type echo-request -j REJECT --reject-with icmp-host-unreachable

# DOPUSZCZONE PORTY
IPORTS=20,21,22,53,69,80,137,138,139,160,161,443,445,514,10050
OPORTS=20,21,22,53,69,80,137,138,139,160,161,443,445,514,10050

# NIE kombinować: porty dla rsyslog, zabbix agent oraz Python(Flask i Django)
# IPORTS_=514,10514,5000,8000,10050
# OPORTS_=514,10514,5000,8000,10050


# REGUŁY
#iptables -A INPUT -p tcp --sport 1024: --dport 49152:65534  -m state --state ESTABLISHED -j ACCEPT
#iptables -A OUTPUT -p tcp --sport 1024: --dport 49152:65534  -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -p tcp --sport 65500:65530 -j ACCEPT
iptables -A INPUT  -p tcp --dport 65500:65530 -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#

iptables -A INPUT -p tcp -m multiport --dport $IPORTS -m state --state NEW -j ACCEPT
iptables -A OUTPUT -p tcp -m multiport --sport $OPORTS -m state --state NEW -j ACCEPT
iptables -A INPUT -p udp -m multiport --dport $IPORTS -m state --state NEW -j ACCEPT
iptables -A OUTPUT -p udp -m multiport --sport $OPORTS -m state --state NEW -j ACCEPT
#iptables -A INPUT -p tcp -m multiport --dport $IPORTS_ -m state --state NEW -j ACCEPT
#iptables -A OUTPUT -p tcp -m multiport --sport $OPORTS_ -m state --state NEW -j ACCEPT
#iptables -A INPUT -p udp -m multiport --dport $IPORTS_ -m state --state NEW -j ACCEPT
#iptables -A OUTPUT -p udp -m multiport --sport $OPORTS_ -m state --state NEW -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT -p tcp -i eth0 -j REJECT --reject-with tcp-reset
iptables -A INPUT -p udp -i eth0 -j REJECT --reject-with icmp-port-unreachable
