#!/bin/bash
LOG_FILE="/var/log/vpn-healer.log"
MAX_RETRIES=3

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOG_FILE"
}

check_and_restart_service() {
    local service_name=$1
    local systemd_name=$2
    local retry_count=0

    # Проверяем, активен ли сервис
    if systemctl is-active --quiet "$systemd_name" 2>/dev/null; then
        log_message "$service_name is running"
        return 0
    fi

    log_message "$service_name is down, attempting to restart..."

    while [ $retry_count -lt $MAX_RETRIES ]; do
        ((retry_count++))
        log_message "Restart attempt $retry_count for $service_name"

        # Перезапускаем сервис
        systemctl restart "$systemd_name" 2>/dev/null
        sleep 5

        if systemctl is-active --quiet "$systemd_name" 2>/dev/null; then
            log_message "$service_name restored successfully after $retry_count attempt(s)"
            return 0
        fi
    done

    log_message "FAILED to restore $service_name after $MAX_RETRIES attempts"
    return 1
}

check_wireguard() {
    # Проверяем интерфейс WireGuard
    if ip link show wg0 >/dev/null 2>&1; then
        log_message "WireGuard interface wg0 exists"
        return 0
    else
        log_message "WireGuard interface wg0 missing, trying to bring up..."
        wg-quick up wg0 2>/dev/null
        sleep 3
        if ip link show wg0 >/dev/null 2>&1; then
            log_message "WireGuard interface wg0 restored"
            return 0
        else
            log_message "FAILED to restore WireGuard interface"
            return 1
        fi
    fi
}

check_cloak() {
    # Проверяем процесс cloak
    if pgrep -f "ck-server" >/dev/null 2>&1; then
        log_message "Cloak server is running"
        return 0
    else
        log_message "Cloak server is down, trying to start..."
        # Запускаем cloak из systemd или напрямую
        systemctl restart cloak 2>/dev/null || {
            # Если systemd сервиса нет, запускаем напрямую
            nohup /usr/local/bin/ck-server -c /etc/cloak/server.json >/dev/null 2>&1 &
            sleep 3
        }
        if pgrep -f "ck-server" >/dev/null 2>&1; then
            log_message "Cloak server restored"
            return 0
        else
            log_message "FAILED to restore Cloak server"
            return 1
        fi
    fi
}

# Основная логика
main() {
    log_message "Starting VPN health check..."

    # Проверяем и восстанавливаем сервисы
    check_and_restart_service "Xray" "xray.service"
    check_and_restart_service "Shadowsocks" "shadowsocks-libev.service"
    check_and_restart_service "Shadowsocks-v2ray" "shadowsocks-v2ray.service"
    check_wireguard
    check_cloak

    # Проверяем порты
    log_message "Checking listening ports..."
    netstat -tulpn | grep -E ":(443|4443|8388|8443)" >> "$LOG_FILE" 2>/dev/null

    log_message "VPN health check completed"
}

# Запускаем основную функцию
main