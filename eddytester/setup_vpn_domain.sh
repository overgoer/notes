#!/bin/bash

# Скрипт автоматической настройки домена и Cloudflare для VPN
# Выполнять на сервере 217.144.185.210 под root

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Настройка домена и Cloudflare для VPN ===${NC}"

# Проверка прав root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Ошибка: скрипт должен выполняться под root${NC}"
  exit 1
fi

# Проверка наличия необходимых утилит
for cmd in curl wget dig; do
  if ! command -v $cmd &> /dev/null; then
    echo -e "${YELLOW}Установка $cmd...${NC}"
    apt-get update && apt-get install -y $cmd
  fi
done

# Запрос параметров
DOMAIN="pupupuuu.com"
echo -e "${GREEN}Домен: ${DOMAIN}${NC}"

echo -e "${GREEN}Введите API токен Cloudflare:${NC}"
read -s CF_API_TOKEN

echo -e "${GREEN}Введите email для уведомлений Let's Encrypt (опционально):${NC}"
read EMAIL

if [ -z "$EMAIL" ]; then
  EMAIL="admin@${DOMAIN}"
fi

# Проверка DNS разрешения домена
echo -e "${YELLOW}Проверка DNS разрешения домена $DOMAIN...${NC}"
if ! dig $DOMAIN +short | grep -q '217.144.185.210'; then
  echo -e "${RED}Предупреждение: домен $DOMAIN не разрешается на IP 217.144.185.210${NC}"
  echo -e "${YELLOW}Убедитесь, что в Cloudflare настроена A-запись с проксированием (оранжевое облако)${NC}"
  read -p "Продолжить? (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Установка Caddy
echo -e "${YELLOW}Установка Caddy...${NC}"
if ! command -v caddy &> /dev/null; then
  apt-get install -y debian-keyring debian-archive-keyring apt-transport-https
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
  apt-get update
  apt-get install -y caddy
else
  echo -e "${GREEN}Caddy уже установлен${NC}"
fi

# Настройка переменных окружения
echo -e "${YELLOW}Настройка переменных окружения...${NC}"
if ! grep -q "CLOUDFLARE_API_TOKEN" /etc/environment; then
  echo "CLOUDFLARE_API_TOKEN=$CF_API_TOKEN" >> /etc/environment
fi
source /etc/environment

# Создание конфигурации Caddy
echo -e "${YELLOW}Создание конфигурации Caddy...${NC}"
cat > /etc/caddy/Caddyfile << EOF
$DOMAIN {
    # Проксирование на Cloak (порт 8443)
    reverse_proxy localhost:8443

    # Автоматический TLS через Cloudflare DNS
    tls {
        dns cloudflare $CLOUDFLARE_API_TOKEN
    }

    # Логирование
    log {
        output file /var/log/caddy/access.log
    }
}

# Резервный доступ по IP (прямой доступ к мониторингу)
:8081 {
    root * /var/www/monitor
    file_server
    basicauth {
        admin $(cat /etc/nginx/.htpasswd | cut -d: -f2)
    }
}
EOF

# Создание директории для логов
mkdir -p /var/log/caddy

# Перезапуск Caddy
echo -e "${YELLOW}Перезапуск Caddy...${NC}"
systemctl restart caddy
systemctl enable caddy

# Проверка статуса Caddy
if systemctl is-active --quiet caddy; then
  echo -e "${GREEN}Caddy успешно запущен${NC}"
else
  echo -e "${RED}Ошибка запуска Caddy${NC}"
  journalctl -u caddy --no-pager -n 20
  exit 1
fi

# Создание скрипта ротации SNI
echo -e "${YELLOW}Создание скрипта ротации SNI...${NC}"
cat > /usr/local/bin/rotate-sni.sh << 'EOF'
#!/bin/bash
# Скрипт ротации SNI для улучшения маскировки трафика

SNI_LIST=(
    "discord.com"
    "cloudflare.com"
    "github.com"
    "google.com"
    "facebook.com"
    "twitter.com"
    "reddit.com"
    "stackoverflow.com"
    "microsoft.com"
    "apple.com"
    "amazon.com"
    "netflix.com"
    "youtube.com"
    "zoom.us"
    "slack.com"
)

# Выбор случайного SNI
RANDOM_SNI=${SNI_LIST[$RANDOM % ${#SNI_LIST[@]}]}

# Обновление конфигурации Xray Reality (если используется)
XRAY_CONFIG="/usr/local/etc/xray/config.json"
if [ -f "$XRAY_CONFIG" ]; then
    sed -i "s/\"serverName\": \".*\"/\"serverName\": \"$RANDOM_SNI\"/" $XRAY_CONFIG
    systemctl restart xray
    echo "$(date): SNI изменён на $RANDOM_SNI для Xray" >> /var/log/sni-rotation.log
fi

# Обновление конфигурации Cloak (если используется)
CLOAK_CONFIG="/etc/cloak/config.json"
if [ -f "$CLOAK_CONFIG" ]; then
    sed -i "s/\"ServerName\": \".*\"/\"ServerName\": \"$RANDOM_SNI\"/" $CLOAK_CONFIG
    systemctl restart cloak
    echo "$(date): SNI изменён на $RANDOM_SNI для Cloak" >> /var/log/sni-rotation.log
fi

echo "SNI ротирован: $RANDOM_SNI"
EOF

chmod +x /usr/local/bin/rotate-sni.sh

# Добавление cron задания для ротации SNI каждые 6 часов
(crontab -l 2>/dev/null | grep -v "rotate-sni.sh"; echo "0 */6 * * * /usr/local/bin/rotate-sni.sh") | crontab -

# Первый запуск ротации SNI
/usr/local/bin/rotate-sni.sh

# Обновление скрипта мониторинга для включения проверки домена
echo -e "${YELLOW}Обновление системы мониторинга...${NC}"
MONITOR_SCRIPT="/usr/local/bin/vpn-monitor.py"
if [ -f "$MONITOR_SCRIPT" ]; then
    # Добавление проверки домена
    sed -i '/# Проверка портов/a\
\    # Проверка доступности домена\
    try:\
        domain_status = check_domain(domain)\
        status_data["domain"] = domain_status\
    except Exception as e:\
        status_data["domain"] = {"status": False, "error": str(e)}' $MONITOR_SCRIPT

    # Добавление функции проверки домена перед существующими функциями
    sed -i '/def check_port(i, host, port):/i\
def check_domain(domain):\
    """Проверка доступности домена"""\
    try:\
        # Проверка DNS разрешения\
        import socket\
        ip = socket.gethostbyname(domain)\
        # Проверка HTTP подключения (порт 443)\
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\
        sock.settimeout(5)\
        result = sock.connect_ex((ip, 443))\
        sock.close()\
        return {"status": result == 0, "ip": ip}\
    except Exception as e:\
        return {"status": False, "error": str(e)}' $MONITOR_SCRIPT

    # Добавление домена в список проверок
    sed -i "s/status_data = {}/status_data = {'domain': '$DOMAIN'}/" $MONITOR_SCRIPT
fi

# Создание тестовой страницы для проверки домена
cat > /var/www/monitor/domain-test.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Проверка домена $DOMAIN</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Проверка домена $DOMAIN</h1>
    <p>Домен: <strong>$DOMAIN</strong></p>
    <p>Сервер IP: <strong>217.144.185.210</strong></p>
    <p>Cloudflare проксирование: <span style="color: green;">Включено</span></p>
    <p>Время: <span id="time"></span></p>
    <script>
        document.getElementById('time').textContent = new Date().toLocaleString();
        setInterval(() => {
            document.getElementById('time').textContent = new Date().toLocaleString();
        }, 1000);
    </script>
</body>
</html>
EOF

# Проверка конфигурации
echo -e "${YELLOW}Проверка конфигурации...${NC}"
caddy validate --config /etc/caddy/Caddyfile

# Открытие портов firewall
echo -e "${YELLOW}Настройка firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw reload
elif command -v iptables &> /dev/null; then
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    iptables-save > /etc/iptables/rules.v4
fi

# Итоговая информация
echo -e "${GREEN}=== Настройка завершена ===${NC}"
echo -e "${GREEN}Домен: $DOMAIN${NC}"
echo -e "${GREEN}Cloudflare проксирование: Включено${NC}"
echo -e "${GREEN}Caddy настроен с автоматическим TLS${NC}"
echo -e "${GREEN}Cloak доступен через: https://$DOMAIN/${NC}"
echo -e "${GREEN}Мониторинг доступен по: http://217.144.185.210:8081/${NC}"
echo -e "${GREEN}Ротация SNI настроена (каждые 6 часов)${NC}"
echo ""
echo -e "${YELLOW}Следующие шаги:${NC}"
echo "1. Проверьте доступность https://$DOMAIN/"
echo "2. Проверьте мониторинг: http://217.144.185.210:8081/"
echo "3. Обновите клиентские конфигурации с новым доменом"
echo "4. Протестируйте VPN подключение через домен"
echo ""
echo -e "${YELLOW}Для отладки:${NC}"
echo "  Журнал Caddy: journalctl -u caddy -f"
echo "  Проверка TLS: curl -I https://$DOMAIN/"
echo "  Ротация SNI: /usr/local/bin/rotate-sni.sh"
echo "  Статус сервисов: systemctl status caddy cloak xray"