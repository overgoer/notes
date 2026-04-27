# План улучшения VPN инфраструктуры

## Текущая конфигурация сервера 217.144.185.210

### Установленные сервисы:
1. **Xray Reality** - порт 443 (TCP)
   - Протокол: VLESS + Reality
   - Имитация: Cloudflare (dest: www.cloudflare.com:443)
   - ServerNames: vkvideo.ru
   - SNI маскировка

2. **Shadowsocks с v2ray-plugin** - порт 4443 (TCP)
   - WebSocket маскировка
   - Метод: chacha20-ietf-poly1305

3. **Shadowsocks обычный** - порт 8388 (TCP/UDP)
   - Используется для Cloak

4. **Cloak** - порт 8443 (TCP)
   - Обфускация трафика
   - Прокси на Shadowsocks 8388

5. **WireGuard** - порт 443 (UDP)
   - Подсеть: 10.10.10.1/24
   - Один пир настроен

6. **OpenVPN** - отключен (порт 443 TCP)
   - Конфигурация сервера существует
   - Клиентский конфиг доступен

7. **Python HTTP сервер** - порт 8080
   - Раздача конфигурационных файлов

## Приоритеты улучшений

### 1. Резервирование и мониторинг (первый этап)

#### Мониторинг:
- **Веб-интерфейс** с минималистичным отображением статуса сервисов
- **Проверка состояния**: systemctl status, listening порты, тестовые подключения
- **Логирование** истории доступности
- **Автоматические оповещения** (telegram/bot)

#### Резервирование:
- **Health checks** для каждого протокола
- **Скрипт автоматического перезапуска** упавших сервисов
- **Резервные конфигурации** на разных портах
- **Подготовка backup сервера** (опционально)

### 2. Улучшение маскировки трафика (второй этап)

#### Доменное имя и CDN:
- Регистрация домена
- Настройка Cloudflare CDN
- Автоматическое TLS (Let's Encrypt)
- Маскировка под обычный веб-сайт

#### Динамическая ротация:
- Автоматическая смена SNI (раз в 6 часов)
- Ротация портов (еженедельно)
- Смена параметров шифрования

#### Улучшение существующих конфигураций:
- Xray: добавление fallback конфигураций
- Shadowsocks: переход на более скрытные плагины
- Cloak: обновление до последней версии

### 3. Добавление новых протоколов (третий этап)

#### Приоритетные протоколы:
1. **Hysteria 2** - UDP-based с маскировкой под QUIC
2. **Tuic** - QUIC протокол от Bilibili
3. **NaïveProxy** - маскировка под обычный HTTPS
4. **Trojan-Go** - с поддержкой WebSocket

#### Стратегия внедрения:
- Поэтапное добавление (один протокол в неделю)
- Тестирование на устойчивость к блокировкам
- Создание клиентских конфигураций

### 4. Удобное получение конфигураций

#### Веб-интерфейс для конфигов:
- Генерация клиентских конфигов по запросу
- QR-коды для мобильных клиентов
- Автоматическая подгонка под устройство

#### API для управления:
- REST API для получения актуальных конфигов
- Авторизация по токену
- Ведение истории изменений

#### Безопасная доставка:
- Шифрование конфигов
- Одноразовые ссылки
- Подтверждение получения

## Детальный план этапа 1: Резервирование и мониторинг

### 1.1 Установка веб-сервера (nginx)
```bash
apt update && apt install -y nginx
```

### 1.2 Создание скрипта мониторинга
**Файл:** `/usr/local/bin/vpn-monitor.py`
```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

SERVICES = [
    {"name": "xray", "port": 443, "type": "tcp"},
    {"name": "shadowsocks-v2ray", "port": 4443, "type": "tcp"},
    {"name": "shadowsocks", "port": 8388, "type": "tcp"},
    {"name": "cloak", "port": 8443, "type": "tcp"},
    {"name": "wireguard", "port": 443, "type": "udp"}
]

def check_service(service_name):
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

def main():
    status = {}
    
    for service in SERVICES:
        service_status = {
            "systemd": check_service(service["name"]),
            "port": check_port(service["port"], service["type"]),
            "timestamp": datetime.now().isoformat()
        }
        service_status["overall"] = service_status["systemd"] and service_status["port"]
        status[service["name"]] = service_status
    
    # Сохранение в JSON
    with open("/var/www/monitor/status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    # Вывод в консоль
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()
```

### 1.3 Веб-интерфейс мониторинга
**Файл:** `/var/www/monitor/index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>VPN Status Monitor</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: monospace; margin: 20px; }
        .service { margin: 10px 0; padding: 10px; border: 1px solid #ccc; }
        .up { background-color: #d4edda; }
        .down { background-color: #f8d7da; }
    </style>
</head>
<body>
    <h1>VPN Services Status</h1>
    <div id="status">Loading...</div>
    <script>
        async function loadStatus() {
            const response = await fetch('/status.json');
            const data = await response.json();
            let html = '';
            for (const [name, info] of Object.entries(data)) {
                const cls = info.overall ? 'up' : 'down';
                html += `<div class="service ${cls}">
                    <strong>${name}</strong><br>
                    Systemd: ${info.systemd ? '✅' : '❌'}<br>
                    Port ${info.port}: ${info.port ? '✅' : '❌'}<br>
                    Updated: ${new Date(info.timestamp).toLocaleString()}
                </div>`;
            }
            document.getElementById('status').innerHTML = html;
        }
        loadStatus();
        setInterval(loadStatus, 30000);
    </script>
</body>
</html>
```

### 1.4 Настройка cron для автоматической проверки
```bash
# Каждые 5 минут
*/5 * * * * /usr/bin/python3 /usr/local/bin/vpn-monitor.py
```

### 1.5 Скрипт автоматического восстановления
**Файл:** `/usr/local/bin/vpn-healer.sh`
```bash
#!/bin/bash
LOG_FILE="/var/log/vpn-healer.log"

SERVICES=("xray" "shadowsocks-libev" "cloak")

for service in "${SERVICES[@]}"; do
    if ! systemctl is-active --quiet $service; then
        echo "$(date): $service is down, restarting..." >> $LOG_FILE
        systemctl restart $service
        sleep 5
        
        if systemctl is-active --quiet $service; then
            echo "$(date): $service restored successfully" >> $LOG_FILE
        else
            echo "$(date): FAILED to restore $service" >> $LOG_FILE
        fi
    fi
done
```

### 1.6 Настройка оповещений (Telegram Bot)
```bash
# Создание бота через @BotFather
# Добавление скрипта отправки сообщений
cat > /usr/local/bin/send-alert.sh << 'EOF'
#!/bin/bash
BOT_TOKEN="your_bot_token"
CHAT_ID="your_chat_id"
MESSAGE="$1"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="${CHAT_ID}" \
    -d text="${MESSAGE}" \
    -d parse_mode="Markdown"
EOF
```

## Детальный план этапа 2: Улучшение маскировки трафика

### Обзор этапа
Цель: улучшить маскировку VPN трафика под легитимный HTTPS трафик через:
1. Регистрацию домена и использование Cloudflare CDN
2. Настройку автоматического TLS (Let's Encrypt)
3. Динамическую ротацию SNI для усложнения обнаружения
4. Интеграцию с существующими сервисами (Cloak через веб-сервер)

### 2.1 Регистрация домена

#### Выбор доменного имени:
- Рекомендуется использовать нейтральные имена, не связанные с VPN:
  - `cloud-access.example.com`
  - `secure-connect.example.com` 
  - `data-relay.example.com`
- Избегать ключевых слов: vpn, proxy, tunnel, ssh
- Использовать популярные TLD: `.com`, `.net`, `.org`

#### Регистрация через регистратора:
1. **Выбор регистратора** (примеры):
   - Namecheap, GoDaddy, Google Domains, Cloudflare Registrar
   - Cloudflare Registrar удобен для последующей интеграции

2. **Процесс регистрации**:
   - Поиск доступного домена
   - Выбор периода регистрации (минимум 1 год)
   - Включение WHOIS privacy (если доступно)
   - Оплата и подтверждение

3. **Настройка DNS записей**:
   - После регистрации добавить A-запись:
     ```
     Имя: @ (или subdomain)
     Тип: A
     Значение: 217.144.185.210 (ваш сервер)
     TTL: Авто
     ```

### 2.2 Настройка Cloudflare CDN

#### Добавление сайта в Cloudflare:
1. **Создание аккаунта** на cloudflare.com (если отсутствует)
2. **Добавление сайта**:
   - Ввести доменное имя
   - Выберите бесплатный план (Free)
   - Cloudflare просканирует существующие DNS записи

3. **Изменение NS серверов**:
   - Cloudflare предоставит 2 NS сервера (например, `lara.ns.cloudflare.com`, `marty.ns.cloudflare.com`)
   - В панели регистратора домена заменить NS сервера на предоставленные Cloudflare
   - Ожидать распространения DNS (до 48 часов, обычно 1-2 часа)

4. **Настройка параметров**:
   - **Проксирование (Orange cloud)**: Включить для A-записи вашего сервера
   - **SSL/TLS**: Режим "Full (strict)"
   - **Always Use HTTPS**: Включить
   - **HTTP/3 (QUIC)**: Включить
   - **WebSockets**: Включить (для Shadowsocks с v2ray-plugin)
   - **Поддержка HTTP/2**: Включить

5. **Получение API токена**:
   - В панели Cloudflare: My Profile → API Tokens
   - Создать токен с правами:
     - Zone.Zone: Read
     - Zone.DNS: Edit
     - Zone.SSL and Certificates: Edit
   - Сохранить токен в безопасном месте

### 2.3 Настройка веб-сервера (Caddy)

#### Установка Caddy:
```bash
# Добавление репозитория Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy
```

#### Настройка переменных окружения:
```bash
# Сохранить Cloudflare API токен
echo "CLOUDFLARE_API_TOKEN=ваш_токен_здесь" | sudo tee -a /etc/environment

# Применить переменные
source /etc/environment
```

#### Конфигурация Caddyfile:
```bash
# Создание конфигурации
sudo tee /etc/caddy/Caddyfile << 'EOF'
your-domain.com {
    # Проксирование на Cloak (порт 8443)
    reverse_proxy localhost:8443
    
    # Автоматический TLS через Cloudflare DNS
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
    
    # Настройки безопасности
    header {
        # Скрытие серверных заголовков
        -Server
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        X-XSS-Protection "1; mode=block"
    }
    
    # Лимиты
    limits {
        header 1mb
        body 10mb
    }
}

# Резервный порт для прямого доступа (без Cloudflare)
:8443 {
    reverse_proxy localhost:8443
}
EOF
```

#### Запуск и проверка:
```bash
# Проверка конфигурации
sudo caddy validate --config /etc/caddy/Caddyfile

# Включение автозапуска
sudo systemctl enable --now caddy

# Проверка статуса
sudo systemctl status caddy
sudo caddy version
```

#### Настройка firewall:
```bash
# Разрешить порты 80 и 443 через firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### 2.4 Интеграция с существующими сервисами

#### Адаптация Cloak для работы через Caddy:
1. **Проверка конфигурации Cloak**:
   ```bash
   # Cloak уже слушает порт 8443 локально
   ss -tuln | grep 8443
   ```

2. **Обновление клиентских конфигураций**:
   - Для Cloak через Cloudflare использовать доменное имя вместо IP
   - Обновить `ServerName` в клиентских конфигах на ваш домен

#### Настройка резервного доступа:
- Прямой доступ к серверу по IP: порт 8443 (Cloak)
- Доступ через Cloudflare: порт 443 (Caddy → Cloak)
- Это обеспечивает отказоустойчивость при блокировке Cloudflare

### 2.5 Динамическая ротация SNI

#### Создание скрипта ротации:
```bash
sudo tee /usr/local/bin/rotate-sni.sh << 'EOF'
#!/bin/bash
# Скрипт ротации SNI для Xray
LOG_FILE="/var/log/sni-rotation.log"

# Список популярных доменов для маскировки
SNI_LIST=(
    "vkvideo.ru"
    "www.youtube.com" 
    "www.google.com"
    "www.microsoft.com"
    "www.github.com"
    "www.amazon.com"
    "www.reddit.com"
    "www.netflix.com"
    "open.spotify.com"
    "connect.facebook.net"
)

# Выбор случайного SNI
RANDOM_SNI=${SNI_LIST[$RANDOM % ${#SNI_LIST[@]}]}

# Логирование
echo "$(date): Rotating SNI to $RANDOM_SNI" >> "$LOG_FILE"

# Обновление конфигурации Xray (если используется Xray)
if [ -f "/usr/local/etc/xray/config.json" ]; then
    # Создание временного файла
    TEMP_FILE=$(mktemp)
    
    # Обновление serverNames в config.json
    jq --arg sni "$RANDOM_SNI" \
       '.inbounds[0].streamSettings.realitySettings.serverNames = [$sni]' \
       /usr/local/etc/xray/config.json > "$TEMP_FILE"
    
    # Проверка и применение
    if jq empty "$TEMP_FILE" 2>/dev/null; then
        mv "$TEMP_FILE" /usr/local/etc/xray/config.json
        systemctl reload xray
        echo "$(date): SNI rotated successfully" >> "$LOG_FILE"
    else
        echo "$(date): ERROR: Invalid JSON generated" >> "$LOG_FILE"
        rm -f "$TEMP_FILE"
    fi
fi

# Также можно обновить другие сервисы (при наличии)
EOF

# Права на выполнение
sudo chmod +x /usr/local/bin/rotate-sni.sh

# Установка jq для обработки JSON
sudo apt install -y jq
```

#### Настройка автоматической ротации:
```bash
# Ротация каждые 6 часов
echo "0 */6 * * * /usr/local/bin/rotate-sni.sh" | sudo tee -a /etc/crontab

# Тестовый запуск
sudo /usr/local/bin/rotate-sni.sh
```

#### Ротация портов (опционально):
```bash
sudo tee /usr/local/bin/rotate-ports.sh << 'EOF'
#!/bin/bash
# Ротация резервных портов
PORTS=(8444 8445 8446 8447 8448)
RANDOM_PORT=${PORTS[$RANDOM % ${#PORTS[@]}]}

# Обновление конфигураций сервисов
# (требуется адаптация под конкретные сервисы)
EOF
```

### 2.6 Тестирование и валидация

#### Проверка TLS сертификата:
```bash
# Проверка выдачи сертификата
curl -I https://your-domain.com
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

#### Тестирование VPN через Cloudflare:
1. **Прямое подключение** (до Cloudflare):
   - Использовать IP:порт (217.144.185.210:8443)
   - Проверить работоспособность Cloak

2. **Подключение через CDN**:
   - Использовать домен:порт (your-domain.com:443)
   - Проверить, что трафик проходит через Cloudflare

#### Проверка маскировки:
```bash
# Анализ трафика с помощью tcpdump
sudo tcpdump -i any port 443 -c 10 -nn

# Проверка HTTP заголовков
curl -v https://your-domain.com
```

### 2.7 Мониторинг и обслуживание

#### Интеграция с системой мониторинга:
```bash
# Добавление проверки домена в мониторинг
sudo tee -a /usr/local/bin/vpn-monitor.py << 'EOF'

def check_domain(domain):
    """Проверка доступности домена"""
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
         f"https://{domain}"],
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout.strip() == "200"
EOF
```

#### Регулярные задачи:
1. **Обновление сертификатов**: Caddy делает это автоматически
2. **Ротация SNI**: Каждые 6 часов (cron)
3. **Проверка доступности**: Интеграция с существующим мониторингом
4. **Резервное копирование конфигураций**: Раз в неделю

### 2.8 Устранение неполадок

#### Распространённые проблемы:
1. **DNS не распространились**: Подождать до 48 часов, проверить через `dig your-domain.com`
2. **Cloudflare не проксирует**: Убедиться, что orange cloud включён для A-записи
3. **Ошибки TLS**: Проверить API токен Cloudflare, права доступа
4. **Блокировка Cloudflare**: Использовать резервный доступ по IP:порт

#### Команды диагностики:
```bash
# Проверка DNS
nslookup your-domain.com
dig your-domain.com

# Проверка SSL
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Проверка проксирования Cloudflare
curl -H "Host: your-domain.com" http://localhost:80
```

### 2.9 Оценка результатов

#### Метрики успеха:
1. **Доступность через домен**: >99.9%
2. **Время подключения**: <2 секунд через Cloudflare
3. **Обнаружение блокировок**: Снижение на 80% по сравнению с прямым IP
4. **Скорость передачи**: Максимально возможная через CDN

#### Дальнейшие улучшения:
1. **Геораспределение**: Добавление серверов в разных регионах
2. **Anycast DNS**: Использование Cloudflare Anycast
3. **DDoS защита**: Включение дополнительной защиты Cloudflare
4. **Аналитика трафика**: Мониторинг паттернов использования

## Детальный план этапа 3: Добавление новых протоколов

### 3.1 Hysteria 2
```bash
# Установка
wget -O /usr/local/bin/hysteria https://github.com/apernet/hysteria/releases/latest/download/hysteria-linux-amd64

# Конфигурация
cat > /etc/hysteria/config.yaml << EOF
listen: :8444
protocol: udp
obfs:
  type: salamander
  salamander:
    password: $(openssl rand -hex 16)
auth:
  type: password
  password: $(openssl rand -hex 32)
EOF
```

### 3.2 Tuic
```bash
# Установка
wget -O /usr/local/bin/tuic-server https://github.com/EAimTY/tuic/releases/latest/download/tuic-server-linux-x86_64

# Конфигурация
cat > /etc/tuic/config.json << EOF
{
  "server": "[::]:8445",
  "users": {
    "user1": "$(openssl rand -hex 32)"
  },
  "congestion_control": "bbr",
  "alpn": ["h3"]
}
EOF
```

## Временная шкала реализации

### Неделя 1: Резервирование и мониторинг
- День 1: Установка веб-сервера и создание скриптов мониторинга
- День 2: Настройка веб-интерфейса и автоматических проверок
- День 3: Реализация скриптов восстановления
- День 4: Настройка оповещений (Telegram)
- День 5: Тестирование и отладка

### Неделя 2: Улучшение маскировки трафика
- День 1: Регистрация домена и настройка Cloudflare
- День 2: Настройка Caddy и TLS
- День 3: Реализация ротации SNI
- День 4: Тестирование маскировки
- День 5: Документирование изменений

### Неделя 3: Добавление новых протоколов
- День 1: Установка и настройка Hysteria 2
- День 2: Установка и настройка Tuic
- День 3: Создание клиентских конфигураций
- День 4: Тестирование протоколов
- День 5: Интеграция в систему мониторинга

### Неделя 4: Финальная оптимизация
- День 1: Настройка геофильтрации и firewall
- День 2: Реализация API для конфигураций
- День 3: Создание веб-интерфейса для управления
- День 4: Стресс-тестирование
- День 5: Документирование всей системы

## Критические файлы для контроля

1. Конфигурации сервисов:
   - `/etc/xray/config.json`
   - `/etc/shadowsocks-libev/config.json`
   - `/etc/shadowsocks-libev/config-v2ray.json`
   - `/etc/cloak/server.json`
   - `/etc/wireguard/wg0.conf`

2. Скрипты мониторинга:
   - `/usr/local/bin/vpn-monitor.py`
   - `/usr/local/bin/vpn-healer.sh`
   - `/usr/local/bin/send-alert.sh`

3. Веб-интерфейс:
   - `/var/www/monitor/index.html`
   - `/var/www/monitor/status.json`

4. Конфигурация веб-сервера:
   - `/etc/nginx/sites-available/monitor`
   - `/etc/caddy/Caddyfile`

## Метрики успеха

1. **Доступность сервисов**: >99.9% uptime
2. **Время восстановления**: <5 минут при сбое
3. **Обнаружение блокировок**: <15 минут
4. **Удобство управления**: веб-интерфейс + API
5. **Безопасность**: регулярная ротация ключей

## Следующие шаги

1. **Немедленно**: Реализация этапа 1 (мониторинг и резервирование)
2. **После завершения**: Документирование результатов
3. **Параллельно**: Подготовка к этапу 2 (домен, Cloudflare)
4. **Долгосрочно**: Постоянное улучшение и адаптация к новым блокировкам