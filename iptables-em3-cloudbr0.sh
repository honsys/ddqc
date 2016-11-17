#!/bin/sh
iptables -A INPUT -i em3 -p icmp --icmp-type echo-reply -j ACCEPT
iptables -A INPUT -i em3 -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT -i cloudbr0 -p icmp --icmp-type echo-reply -j ACCEPT
iptables -A INPUT -i cloudbr0 -p icmp --icmp-type echo-request -j ACCEPT

iptables -A OUTPUT -o em3 -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -o em3 -p icmp --icmp-type echo-reply -j ACCEPT
iptables -A OUTPUT -o cloudbr0 -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -o cloudbr0 -p icmp --icmp-type echo-reply -j ACCEPT
