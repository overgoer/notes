#!/usr/bin/env python3
import base64
import json
import os
import qrcode
import secrets
from nacl.public import PrivateKey as Curve25519PrivateKey

# Папка для выходных файлов
OUTPUT_DIR = "vpn_configs_april_2026"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_qrcode(data, filename):
    """Создать QR-код и сохранить как PNG"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(OUTPUT_DIR, filename))

def save_text(text, filename):
    """Сохранить текстовый файл"""
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        f.write(text)

def x25519_private_to_public(private_key_b64):
    """Конвертировать приватный ключ X25519 (base64) в публичный"""
    # Добавляем padding если необходимо
    padding = 4 - len(private_key_b64) % 4
    if padding != 4:
        private_key_b64 += "=" * padding
    private_key_bytes = base64.b64decode(private_key_b64)
    # Создаем объект приватного ключа NaCl
    private_key = Curve25519PrivateKey(private_key_bytes)
    public_key = private_key.public_key
    public_key_b64 = base64.b64encode(public_key.encode()).decode()
    return public_key_b64

# Данные с сервера (из предыдущей конфигурации)
SERVER_IP = "217.144.185.210"
DOMAIN = "pupupuuu.com"

print("Генерация новых конфигураций для VPN сервисов...")

# 1. Xray Reality на порту 8444
print("1. Генерация XRay Reality (порт 8444)...")
xray_private_key = "iDv6aJYDnkqzwGjO1nKk72JHUjURQWqn8VMyIAMUkGU"
xray_public_key = x25519_private_to_public(xray_private_key)
xray_short_id = "b8e333e47e108af2"
xray_server_name = "vkvideo.ru"
xray_uuid = "25a3a542-20bd-4885-be9d-86813acdd623"
xray_flow = "xtls-rprx-vision"
xray_port = 8444  # Новый порт

# Ссылка VLESS+Reality для приложения Shadowrocket
vless_reality_link = f"vless://{xray_uuid}@{SERVER_IP}:{xray_port}?flow={xray_flow}&encryption=none&security=reality&pbk={xray_public_key}&sni={xray_server_name}&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality+8444"
save_text(vless_reality_link, "xray_reality_8444_url.txt")
save_qrcode(vless_reality_link, "xray_reality_8444_qr.png")
print(f"  Создано: xray_reality_8444_url.txt, xray_reality_8444_qr.png")

# 2. Cloak через домен pupupuuu.com на порту 443
print("2. Генерация Cloak через домен (порт 443)...")
cloak_private_key = "eA8tJEjKqbdm8oLpdvZANdmv1lkane1n4VhNlvoYCUU="
cloak_public_key = x25519_private_to_public(cloak_private_key)
cloak_admin_uid = "WoSu0dWehLioafdctCsiVQ=="
cloak_port = 443  # Порт через домен
cloak_domain = DOMAIN

# Для Cloak нужен UID пользователя. Сгенерируем случайный (base64 16 bytes)
cloak_user_uid = base64.b64encode(secrets.token_bytes(16)).decode()
# Ссылка cloak (формат ss:// с плагином cloak)
cloak_password = secrets.token_hex(12)
cloak_link = f"ss://{base64.b64encode(f'chacha20-ietf-poly1305:{cloak_password}'.encode()).decode()}@{cloak_domain}:{cloak_port}?plugin=ck-client&Transport=direct&UID={cloak_user_uid}&PublicKey={cloak_public_key}&ServerName={cloak_domain}&NumConn=4&BufferSize=4096#Cloak+Domain+443"
save_text(cloak_link, "cloak_domain_url.txt")
save_qrcode(cloak_link, "cloak_domain_qr.png")
print(f"  Создано: cloak_domain_url.txt, cloak_domain_qr.png")

# 3. Shadowsocks Basic на порту 8388
print("3. Генерация Shadowsocks Basic (порт 8388)...")
ss_password = "L0s61BgJ6fhY"
ss_method = "chacha20-ietf-poly1305"
ss_port = 8388
# Ссылка ss://
ss_link = f"ss://{base64.b64encode(f'{ss_method}:{ss_password}'.encode()).decode()}@{SERVER_IP}:{ss_port}#Shadowsocks+Basic+8388"
save_text(ss_link, "shadowsocks_basic_url.txt")
save_qrcode(ss_link, "shadowsocks_basic_qr.png")
print(f"  Создано: shadowsocks_basic_url.txt, shadowsocks_basic_qr.png")

# 4. Также создадим конфигурацию Cloak через IP на порту 8443 (оригинальная)
print("4. Генерация Cloak через IP (порт 8443)...")
cloak_ip_user_uid = base64.b64encode(secrets.token_bytes(16)).decode()
cloak_ip_password = secrets.token_hex(12)
cloak_ip_link = f"ss://{base64.b64encode(f'chacha20-ietf-poly1305:{cloak_ip_password}'.encode()).decode()}@{SERVER_IP}:8443?plugin=ck-client&Transport=direct&UID={cloak_ip_user_uid}&PublicKey={cloak_public_key}&ServerName={SERVER_IP}&NumConn=4&BufferSize=4096#Cloak+IP+8443"
save_text(cloak_ip_link, "cloak_ip_url.txt")
save_qrcode(cloak_ip_link, "cloak_ip_qr.png")
print(f"  Создано: cloak_ip_url.txt, cloak_ip_qr.png")

# 5. Xray Reality на порту 443 (оригинальная)
print("5. Генерация XRay Reality (порт 443)...")
xray_port_443 = 443
vless_reality_link_443 = f"vless://{xray_uuid}@{SERVER_IP}:{xray_port_443}?flow={xray_flow}&encryption=none&security=reality&pbk={xray_public_key}&sni={xray_server_name}&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality+443"
save_text(vless_reality_link_443, "xray_reality_443_url.txt")
save_qrcode(vless_reality_link_443, "xray_reality_443_qr.png")
print(f"  Создано: xray_reality_443_url.txt, xray_reality_443_qr.png")

# Создать README файл
readme = f"""
Конфигурации VPN для сервера {SERVER_IP}
Домен: {DOMAIN}
Сгенерировано: {os.path.basename(__file__)}
Дата: 2026-04-16

Доступные протоколы:
1. Xray Reality (порт 8444) - маскировка под Cloudflare (новый порт)
2. Xray Reality (порт 443) - маскировка под Cloudflare (оригинальный порт)
3. Cloak через домен {DOMAIN} (порт 443) - обфускация через домен
4. Cloak через IP (порт 8443) - обфускация через прямой IP
5. Shadowsocks Basic (порт 8388) - простой шифрованный прокси

Файлы:
- xray_reality_8444_url.txt - ссылка VLESS+Reality на порту 8444
- xray_reality_8444_qr.png - QR-код для порта 8444
- xray_reality_443_url.txt - ссылка VLESS+Reality на порту 443
- xray_reality_443_qr.png - QR-код для порта 443
- cloak_domain_url.txt - ссылка Cloak через домен {DOMAIN}:443
- cloak_domain_qr.png - QR-код для Cloak через домен
- cloak_ip_url.txt - ссылка Cloak через IP {SERVER_IP}:8443
- cloak_ip_qr.png - QR-код для Cloak через IP
- shadowsocks_basic_url.txt - ссылка Shadowsocks Basic
- shadowsocks_basic_qr.png - QR-код для Shadowsocks Basic

Используйте QR-коды для быстрой настройки в приложениях.
Рекомендуемые приложения: Shadowrocket (iOS), v2rayNG (Android), Clash.
"""
save_text(readme, "README.md")

print(f"\nВсе конфигурации успешно сгенерированы в папке {OUTPUT_DIR}/")
print(f"Создано файлов: {len(os.listdir(OUTPUT_DIR))}")