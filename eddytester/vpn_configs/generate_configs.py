#!/usr/bin/env python3
import base64
import json
import os
import qrcode
from nacl.public import PrivateKey as Curve25519PrivateKey

# Папка для выходных файлов
OUTPUT_DIR = "output"
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

# Данные с сервера (заполнены вручную)
SERVER_IP = "217.144.185.210"

# 1. Xray Reality
xray_private_key = "iDv6aJYDnkqzwGjO1nKk72JHUjURQWqn8VMyIAMUkGU"
xray_public_key = x25519_private_to_public(xray_private_key)
xray_short_id = "b8e333e47e108af2"
xray_server_name = "vkvideo.ru"
xray_uuid = "25a3a542-20bd-4885-be9d-86813acdd623"
xray_flow = "xtls-rprx-vision"
xray_port = 443

# Ссылка VLESS+Reality для приложения Shadowrocket
vless_reality_link = f"vless://{xray_uuid}@{SERVER_IP}:{xray_port}?flow={xray_flow}&encryption=none&security=reality&pbk={xray_public_key}&sni={xray_server_name}&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality"
save_text(vless_reality_link, "xray_reality_link.txt")
save_qrcode(vless_reality_link, "xray_reality_qr.png")

# 2. Shadowsocks обычный (порт 8388)
ss_password = "L0s61BgJ6fhY"
ss_method = "chacha20-ietf-poly1305"
ss_port = 8388
# Ссылка ss://
ss_link = f"ss://{base64.b64encode(f'{ss_method}:{ss_password}'.encode()).decode()}@{SERVER_IP}:{ss_port}#Shadowsocks+Basic"
save_text(ss_link, "shadowsocks_basic_link.txt")
save_qrcode(ss_link, "shadowsocks_basic_qr.png")

# 3. Shadowsocks с v2ray-plugin (WebSocket)
ss_v2ray_password = "L0s61BgJ6fhY"
ss_v2ray_method = "chacha20-ietf-poly1305"
ss_v2ray_port = 4443
ss_v2ray_host = SERVER_IP
ss_v2ray_path = "/v2ray"
# Ссылка ss:// с плагином (специальный формат для Shadowrocket)
plugin_opts = f"obfs=websocket;obfs-host={ss_v2ray_host};obfs-uri={ss_v2ray_path}"
ss_v2ray_link = f"ss://{base64.b64encode(f'{ss_v2ray_method}:{ss_v2ray_password}'.encode()).decode()}@{SERVER_IP}:{ss_v2ray_port}?plugin=v2ray-plugin&{plugin_opts}#Shadowsocks+v2ray+WebSocket"
save_text(ss_v2ray_link, "shadowsocks_v2ray_link.txt")
save_qrcode(ss_v2ray_link, "shadowsocks_v2ray_qr.png")

# 4. Cloak
cloak_private_key = "eA8tJEjKqbdm8oLpdvZANdmv1lkane1n4VhNlvoYCUU="
cloak_public_key = x25519_private_to_public(cloak_private_key)
cloak_admin_uid = "WoSu0dWehLioafdctCsiVQ=="
cloak_port = 8443
# Для Cloak нужен UID пользователя. Сгенерируем случайный (base64 16 bytes)
import secrets
cloak_user_uid = base64.b64encode(secrets.token_bytes(16)).decode()
# Ссылка cloak (формат ss:// с плагином cloak)
cloak_link = f"ss://{base64.b64encode(f'chacha20-ietf-poly1305:{secrets.token_hex(12)}'.encode()).decode()}@{SERVER_IP}:{cloak_port}?plugin=ck-client&Transport=direct&UID={cloak_user_uid}&PublicKey={cloak_public_key}&ServerName={SERVER_IP}&NumConn=4&BufferSize=4096#Cloak"
save_text(cloak_link, "cloak_link.txt")
save_qrcode(cloak_link, "cloak_qr.png")

# 5. WireGuard
# Нужен клиентский приватный ключ. Сгенерируем новый.
wireguard_client_private_key = base64.b64encode(os.urandom(32)).decode()
# Публичный ключ клиента
from nacl.public import PrivateKey as WGPrivateKey
wg_priv = WGPrivateKey(base64.b64decode(wireguard_client_private_key))
wg_pub = base64.b64encode(wg_priv.public_key.encode()).decode()
# Серверный публичный ключ из конфига (пока неизвестен). Используем существующий пир.
# Из конфига сервера: публичный ключ пира HvL9lg+BHmgdyz0tSIpx6ZXQT/ePnsEdZPhIirpOrEo=
# Прешаренный ключ tpedSgKfjJ6fOSf7syixQtopv4yk3Uf2fBgdeiyEca0=
wg_server_public_key = "HvL9lg+BHmgdyz0tSIpx6ZXQT/ePnsEdZPhIirpOrEo="
wg_preshared_key = "tpedSgKfjJ6fOSf7syixQtopv4yk3Uf2fBgdeiyEca0="
wg_client_ip = "10.10.10.2/32"
wg_server_endpoint = f"{SERVER_IP}:443"
# Конфиг WireGuard
wg_config = f"""[Interface]
PrivateKey = {wireguard_client_private_key}
Address = {wg_client_ip}
DNS = 8.8.8.8

[Peer]
PublicKey = {wg_server_public_key}
PresharedKey = {wg_preshared_key}
Endpoint = {wg_server_endpoint}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
save_text(wg_config, "wireguard_client.conf")
save_qrcode(wg_config, "wireguard_qr.png")

# 6. Описание приложений для iPhone
apps_description = """
Руководство по приложениям для iPhone:

1. **Xray Reality**:
   - Приложение: Shadowrocket (платное) или Streisand (бесплатное)
   - Использовать ссылку vless:// или импортировать QR-код

2. **Shadowsocks Basic**:
   - Приложение: Shadowrocket, Outline, Potatso Lite
   - Использовать ссылку ss:// или QR-код

3. **Shadowsocks с v2ray-plugin (WebSocket)**:
   - Приложение: Shadowrocket (поддержка плагинов)
   - Требуется включить плагин v2ray-plugin

4. **Cloak**:
   - Приложение: Shadowrocket с поддержкой cloak-plugin
   - Или использовать официальный клиент Cloak

5. **WireGuard**:
   - Приложение: WireGuard (официальное, бесплатное)
   - Импортировать конфиг .conf или отсканировать QR-код

Рекомендации:
- Shadowrocket поддерживает все протоколы, но стоит $2.99
- Для WireGuard используйте официальное приложение
- Настройте автоматическое подключение при запуске
"""
save_text(apps_description, "iphone_apps_guide.txt")

# Создать сводный файл README
readme = f"""
Конфигурации VPN для сервера {SERVER_IP}
Сгенерировано: {os.path.basename(__file__)}

Доступные протоколы:
1. Xray Reality (порт {xray_port}) - маскировка под Cloudflare
2. Shadowsocks Basic (порт {ss_port}) - простой шифрованный прокси
3. Shadowsocks с v2ray-plugin (порт {ss_v2ray_port}) - WebSocket маскировка
4. Cloak (порт {cloak_port}) - обфускация трафика
5. WireGuard (порт 443 UDP) - современный VPN

Файлы:
- xray_reality_link.txt - ссылка VLESS+Reality
- xray_reality_qr.png - QR-код
- shadowsocks_basic_link.txt - ссылка Shadowsocks
- shadowsocks_basic_qr.png - QR-код
- shadowsocks_v2ray_link.txt - ссылка Shadowsocks с WebSocket
- shadowsocks_v2ray_qr.png - QR-код
- cloak_link.txt - ссылка Cloak
- cloak_qr.png - QR-код
- wireguard_client.conf - конфиг WireGuard
- wireguard_qr.png - QR-код для WireGuard
- iphone_apps_guide.txt - руководство по приложениям

Используйте QR-коды для быстрой настройки в приложениях.
"""
save_text(readme, "README.md")

print(f"Конфигурации сгенерированы в папке {OUTPUT_DIR}/")