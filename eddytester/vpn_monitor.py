#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

SERVICES = [
    {"name": "xray", "port": 443, "type": "tcp", "service": "xray.service"},
    {"name": "shadowsocks-v2ray", "port": 4443, "type": "tcp", "service": "shadowsocks-v2ray.service"},
    {"name": "shadowsocks", "port": 8388, "type": "tcp", "service": "shadowsocks-libev.service"},
    {"name": "cloak", "port": 8443, "type": "tcp", "service": "ck-server"},
    {"name": "wireguard", "port": 443, "type": "udp", "service": "wg0-interface"}
]

def check_service(service_name):
    if service_name == "wg0-interface":
        # Проверяем интерфейс WireGuard
        result = subprocess.run(
            ["ip", "link", "show", "wg0"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and "UP" in result.stdout
    elif service_name == "ck-server":
        # Проверяем процесс cloak
        result = subprocess.run(
            ["pgrep", "-f", "ck-server"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    else:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "active"

def check_port(port, proto="tcp"):
    result = subprocess.run(
        ["netstat", "-tulpn"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.split('\n')
    for line in lines:
        if f":{port}" in line and proto in line.lower():
            return True
    return False

def check_connectivity(port, proto="tcp"):
    if proto == "tcp":
        result = subprocess.run(
            ["timeout", "2", "nc", "-z", "localhost", str(port)],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    else:  # udp
        # Для UDP проверка сложнее, просто проверим что порт слушается
        return check_port(port, proto)

def main():
    status = {}

    for service in SERVICES:
        service_name = service["name"]
        service_status = {
            "systemd": check_service(service["service"]),
            "port": check_port(service["port"], service["type"]),
            "connectivity": check_connectivity(service["port"], service["type"]),
            "timestamp": datetime.now().isoformat()
        }
        # Общий статус: все три проверки должны быть True
        service_status["overall"] = (
            service_status["systemd"] and
            service_status["port"] and
            service_status["connectivity"]
        )
        status[service_name] = service_status

    # Сохранение в JSON
    with open("/var/www/monitor/status.json", "w") as f:
        json.dump(status, f, indent=2)

    # Вывод в консоль для отладки
    print(json.dumps(status, indent=2))
    return 0

if __name__ == "__main__":
    exit(main())