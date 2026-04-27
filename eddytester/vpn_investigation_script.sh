#!/bin/bash

# VPN Investigation Script for 217.144.185.210
# Run this on the target server to collect diagnostic information

echo "=== VPN Investigation Report ==="
echo "Generated on: $(date)"
echo "Server: $(hostname) ($(hostname -I))"
echo ""

# System information
echo "=== System Information ==="
uname -a
cat /etc/os-release 2>/dev/null | head -5
echo ""

# WireGuard status
echo "=== WireGuard Status ==="
which wg
which wg-quick
systemctl list-units | grep -i wireguard
systemctl is-active wg-quick@* 2>/dev/null | grep -v "no unit"
wg show 2>/dev/null || echo "WireGuard interface not running"
echo ""

# Configuration files
echo "=== WireGuard Configuration Files ==="
ls -la /etc/wireguard/ 2>/dev/null || echo "/etc/wireguard/ directory not found"
if [ -d "/etc/wireguard/" ]; then
  for conf in /etc/wireguard/*.conf; do
    if [ -f "$conf" ]; then
      echo "Configuration: $conf"
      echo "---"
      grep -v "^#" "$conf" | grep -v "^$" | head -10
      echo "... (truncated)"
      echo "---"
    fi
  done
fi
echo ""

# Network configuration
echo "=== Network Configuration ==="
ip a | grep -E "(inet|link)"
ip route show
echo ""

# Firewall status
echo "=== Firewall Status ==="
ufw status verbose 2>/dev/null || echo "ufw not installed"
iptables -L -n -v 2>/dev/null | head -15 || echo "iptables not available"
echo ""

# TimeWeb server check
echo "=== TimeWeb Server Check ==="
ss -tuln | grep -i "time\|217\.144\.185\.210" || echo "No obvious TimeWeb connections found"
netstat -tuln 2>/dev/null | grep -i "time\|217\.144\.185\.210" || echo ""
echo ""

# DNS configuration
echo "=== DNS Configuration ==="
cat /etc/resolv.conf 2>/dev/null || echo "/etc/resolv.conf not found"

# End report
echo "=== End of Report ==="