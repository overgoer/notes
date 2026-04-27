# Инструкция по созданию QR-кодов на сервере

## Созданные файлы на локальной машине

На локальной машине созданы следующие файлы в папке `/Users/eddy/Downloads/content/vault/eddytester/vpn_configs_april_2026/`:

### Основные конфигурации (по заданию):
1. **XRay Reality (порт 8444)**:
   - `xray_reality_8444_url.txt` - ссылка для подключения
   - `xray_reality_8444_qr.png` - QR-код

2. **Cloak через домен pupupuuu.com (порт 443)**:
   - `cloak_domain_url.txt` - ссылка для подключения
   - `cloak_domain_qr.png` - QR-код

3. **Shadowsocks Basic (порт 8388)**:
   - `shadowsocks_basic_url.txt` - ссылка для подключения
   - `shadowsocks_basic_qr.png` - QR-код

### Дополнительные конфигурации:
4. **Cloak через IP (порт 8443)**:
   - `cloak_ip_url.txt` - ссылка для подключения
   - `cloak_ip_qr.png` - QR-код

5. **XRay Reality (порт 443)**:
   - `xray_reality_443_url.txt` - ссылка для подключения
   - `xray_reality_443_qr.png` - QR-код

## Содержимое URL-ссылок:

### 1. XRay Reality (8444):
```
vless://25a3a542-20bd-4885-be9d-86813acdd623@217.144.185.210:8444?flow=xtls-rprx-vision&encryption=none&security=reality&pbk=3/wrNXs3QnGJudD2oKZNZOhVbRvQFjWOZbd60c1KJR4=&sni=vkvideo.ru&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality+8444
```

### 2. Cloak через домен pupupuuu.com (443):
```
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTphNzQxZThkYTRlMTMxYjMxZmQ3NWE2ODE=@pupupuuu.com:443?plugin=ck-client&Transport=direct&UID=31l+AUm4K2beV6dMX5+OYw==&PublicKey=E4yguFm48fa5myr2yQYZPDb1sqANTE1cV522sqPO5HU=&ServerName=pupupuuu.com&NumConn=4&BufferSize=4096#Cloak+Domain+443
```

### 3. Shadowsocks Basic (8388):
```
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpMMHM2MUJnSjZmaFk=@217.144.185.210:8388#Shadowsocks+Basic+8388
```

## Инструкция для копирования на сервер

### Вариант 1: Использование скрипта (рекомендуется)

1. Скопируйте содержимое скрипта `create_server_qrcodes.sh` на сервер:
   ```bash
   # На локальной машине просмотрите скрипт:
   cat /Users/eddy/Downloads/content/vault/eddytester/create_server_qrcodes.sh
   
   # Скопируйте его содержимое и вставьте в файл на сервере:
   # На сервере выполните:
   nano /tmp/create_qr.sh
   # Вставьте содержимое скрипта, сохраните (Ctrl+X, Y, Enter)
   ```

2. Запустите скрипт на сервере:
   ```bash
   chmod +x /tmp/create_qr.sh
   bash /tmp/create_qr.sh
   ```

3. Скрипт автоматически:
   - Установит `qrencode` если не установлен
   - Создаст директорию `/root/qr_codes/`
   - Сгенерирует все QR-коды и текстовые файлы
   - Создаст README файл

### Вариант 2: Ручное копирование файлов

Если есть доступ по SCP или другой метод копирования:

1. Создайте директорию на сервере:
   ```bash
   mkdir -p /root/qr_codes
   ```

2. Скопируйте файлы с локальной машины на сервер:
   ```bash
   # Пример команды SCP (требует SSH доступ):
   scp /Users/eddy/Downloads/content/vault/eddytester/vpn_configs_april_2026/* root@217.144.185.210:/root/qr_codes/
   ```

### Вариант 3: Использование cat для передачи содержимого

Если нет прямого доступа по SCP, можно передать содержимое файлов через cat:

1. На сервере создайте файл:
   ```bash
   cat > /root/qr_codes/xray_reality_8444_url.txt << 'EOF'
   vless://25a3a542-20bd-4885-be9d-86813acdd623@217.144.185.210:8444?flow=xtls-rprx-vision&encryption=none&security=reality&pbk=3/wrNXs3QnGJudD2oKZNZOhVbRvQFjWOZbd60c1KJR4=&sni=vkvideo.ru&fp=chrome&type=http&path=/api/v1/update&mode=packet-up#Xray+Reality+8444
   EOF
   ```

2. Повторите для остальных файлов.

## Проверка созданных файлов

После выполнения скрипта на сервере проверьте:
```bash
ls -la /root/qr_codes/
```

Должны быть созданы 10 файлов (5 .txt и 5 .png) плюс README.md.

## Примечания

1. **Проверка QR-кодов**: Убедитесь, что QR-коды читаются приложениями (Shadowrocket, v2rayNG и т.д.)
2. **Актуальность портов**: Убедитесь, что сервисы работают на указанных портах:
   - XRay Reality: порт 8444 (и 443)
   - Cloak: порт 443 (через домен) и 8443 (через IP)
   - Shadowsocks: порт 8388
3. **Домен pupupuuu.com**: Должен быть настроен в Cloudflare и указывать на IP сервера 217.144.185.210
4. **Безопасность**: Файлы содержат конфиденциальные данные (ключи, пароли). Храните их в безопасном месте.

## Устранение неполадок

Если QR-коды не генерируются:
1. Проверьте наличие `qrencode`: `which qrencode`
2. Установите: `apt-get install -y qrencode`
3. Проверьте права на запись в `/root/qr_codes/`

Если ссылки не работают:
1. Проверьте, что сервисы запущены: `systemctl status xray`, `systemctl status cloak`
2. Проверьте открыты ли порты: `netstat -tulpn | grep -E '8444|443|8388|8443'`
3. Проверьте firewall: `iptables -L -n`