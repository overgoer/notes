#!/bin/bash

# Скрипт для создания QR-кодов на сервере
# Выполнить на сервере: bash create_server_qrcodes.sh

SERVER_IP="217.144.185.210"
DOMAIN="pupupuuu.com"
QR_DIR="/root/qr_codes"

# Создать директорию если не существует
mkdir -p "$QR_DIR"

# Проверить наличие qrencode
if ! command -v qrencode &> /dev/null; then
    echo "Установка qrencode..."
    apt-get update && apt-get install -y qrencode
fi

echo "Создание QR-кодов в $QR_DIR..."

# 1. XRay Reality на порту 8444
XRAY_URL="vless://25a3a542-20bd-4885-be9d-86813acdd623@${SERVER_IP}:8444?flow=xtls-rprx-vision&encryption=none&security=reality&pbk=3/wrNXs3QnGJudD2oKZNZOhVbRvQFjWOZbd60c1KJR4=&sni=vkvideo.ru&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality+8444"
echo "$XRAY_URL" > "$QR_DIR/xray_reality_8444_url.txt"
qrencode -o "$QR_DIR/xray_reality_8444_qr.png" "$XRAY_URL"
echo "Создан XRay Reality (8444)"

# 2. Cloak через домен на порту 443
CLOAK_DOMAIN_URL="ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTphNzQxZThkYTRlMTMxYjMxZmQ3NWE2ODE=@${DOMAIN}:443?plugin=ck-client&Transport=direct&UID=31l+AUm4K2beV6dMX5+OYw==&PublicKey=E4yguFm48fa5myr2yQYZPDb1sqANTE1cV522sqPO5HU=&ServerName=${DOMAIN}&NumConn=4&BufferSize=4096#Cloak+Domain+443"
echo "$CLOAK_DOMAIN_URL" > "$QR_DIR/cloak_domain_url.txt"
qrencode -o "$QR_DIR/cloak_domain_qr.png" "$CLOAK_DOMAIN_URL"
echo "Создан Cloak через домен (443)"

# 3. Shadowsocks Basic на порту 8388
SS_URL="ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpMMHM2MUJnSjZmaFk=@${SERVER_IP}:8388#Shadowsocks+Basic+8388"
echo "$SS_URL" > "$QR_DIR/shadowsocks_basic_url.txt"
qrencode -o "$QR_DIR/shadowsocks_basic_qr.png" "$SS_URL"
echo "Создан Shadowsocks Basic (8388)"

# 4. Cloak через IP на порту 8443
CLOAK_IP_URL="ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTphNzQxZThkYTRlMTMxYjMxZmQ3NWE2ODE=@${SERVER_IP}:8443?plugin=ck-client&Transport=direct&UID=31l+AUm4K2beV6dMX5+OYw==&PublicKey=E4yguFm48fa5myr2yQYZPDb1sqANTE1cV522sqPO5HU=&ServerName=${SERVER_IP}&NumConn=4&BufferSize=4096#Cloak+IP+8443"
echo "$CLOAK_IP_URL" > "$QR_DIR/cloak_ip_url.txt"
qrencode -o "$QR_DIR/cloak_ip_qr.png" "$CLOAK_IP_URL"
echo "Создан Cloak через IP (8443)"

# 5. XRay Reality на порту 443
XRAY_443_URL="vless://25a3a542-20bd-4885-be9d-86813acdd623@${SERVER_IP}:443?flow=xtls-rprx-vision&encryption=none&security=reality&pbk=3/wrNXs3QnGJudD2oKZNZNZOhVbRvQFjWOZbd60c1KJR4=&sni=vkvideo.ru&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality+443"
echo "$XRAY_443_URL" > "$QR_DIR/xray_reality_443_url.txt"
qrencode -o "$QR_DIR/xray_reality_443_qr.png" "$XRAY_443_URL"
echo "Создан XRay Reality (443)"

# Создать README
cat > "$QR_DIR/README.md" << EOM
QR-коды и ссылки для VPN сервера ${SERVER_IP}
Домен: ${DOMAIN}
Создано: $(date)

Доступные протоколы:
1. Xray Reality (порт 8444) - маскировка под Cloudflare (новый порт)
2. Xray Reality (порт 443) - маскировка под Cloudflare (оригинальный порт)
3. Cloak через домен ${DOMAIN} (порт 443) - обфускация через домен
4. Cloak через IP (порт 8443) - обфускация через прямой IP
5. Shadowsocks Basic (порт 8388) - простой шифрованный прокси

Файлы:
- xray_reality_8444_url.txt - ссылка VLESS+Reality на порту 8444
- xray_reality_8444_qr.png - QR-код для порта 8444
- xray_reality_443_url.txt - ссылка VLESS+Reality на порту 443
- xray_reality_443_qr.png - QR-код для порта 443
- cloak_domain_url.txt - ссылка Cloak через домен ${DOMAIN}:443
- cloak_domain_qr.png - QR-код для Cloak через домен
- cloak_ip_url.txt - ссылка Cloak через IP ${SERVER_IP}:8443
- cloak_ip_qr.png - QR-код для Cloak через IP
- shadowsocks_basic_url.txt - ссылка Shadowsocks Basic
- shadowsocks_basic_qr.png - QR-код для Shadowsocks Basic

Используйте QR-коды для быстрой настройки в приложениях.
EOM

echo "Готово! Все файлы созданы в $QR_DIR/"
ls -la "$QR_DIR/"
