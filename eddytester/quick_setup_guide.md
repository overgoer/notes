# Быстрая настройка домена pupupuuu.com

## Текущий статус
✅ NS серверы уже Cloudflare (`mona.ns.cloudflare.com`, `remy.ns.cloudflare.com`)
✅ Домен зарегистрирован через Cloudflare Registrar
➡️ **Требуется: добавить A-запись и создать API токен**

## Шаг 1: Добавление A-записи (2 минуты)

1. **Откройте панель Cloudflare**: https://dash.cloudflare.com/
2. **Выберите домен** `pupupuuu.com`
3. **Перейдите**: DNS → Records
4. **Нажмите**: "Add record"
5. **Заполните**:
   - Type: **A**
   - Name: **`@`** (корневой домен)
   - IPv4 address: **`217.144.185.210`**
   - Proxy status: **Оранжевое облако** (включено ✓)
   - TTL: Auto
6. **Нажмите**: "Save"

## Шаг 2: Создание API токена (2 минуты)

1. **Вверху справа**: My Profile → API Tokens
2. **Нажмите**: "Create Token"
3. **Выберите шаблон**: **"Edit zone DNS"**
4. **В разделе "Zone Resources"**:
   - Resource: Include → Specific zone
   - Zone: `pupupuuu.com`
5. **Нажмите**: "Continue to summary"
6. **Нажмите**: "Create Token"
7. **СКОПИРУЙТЕ токен** и сохраните в безопасном месте

## Шаг 3: Проверка (1 минута)

В терминале выполните:
```bash
dig pupupuuu.com
```
**Должно вернуть**: `217.144.185.210`

## Шаг 4: Запуск автоматизации на сервере

### Вариант A: Через SCP (если есть доступ)
```bash
# С локального компьютера
scp setup_vpn_domain.sh root@217.144.185.210:/root/
```

### Вариант B: Вручную на сервере
```bash
# На сервере (через SSH)
nano /root/setup_vpn_domain.sh
# Вставьте содержимое файла setup_vpn_domain.sh
# Сохраните: Ctrl+X, Y, Enter
```

### Запуск скрипта:
```bash
# На сервере
chmod +x /root/setup_vpn_domain.sh
cd /root
./setup_vpn_domain.sh
```

**Скрипт запросит**:
1. API токен Cloudflare (вставьте скопированный токен)
2. Email для Let's Encrypt (можно нажать Enter)

## Что сделает скрипт:
- ✅ Установит и настроит Caddy (веб-сервер)
- ✅ Настроит автоматический TLS через Cloudflare
- ✅ Подключит Cloak через reverse proxy
- ✅ Настроит ротацию SNI каждые 6 часов
- ✅ Обновит систему мониторинга

## Проверка после запуска:
1. **TLS сертификат**: `curl -I https://pupupuuu.com/` (без ошибок SSL)
2. **Мониторинг**: `http://217.144.185.210:8081/` (логин: `admin`, пароль: `/mBZIzZFzdqPdyme`)
3. **VPN через домен**: Подключитесь через Cloak с сервером `pupupuuu.com:443`

## Если проблемы:
- **DNS не разрешается**: Подождите 5-10 минут, проверьте `dig pupupuuu.com`
- **Ошибка SSL**: Проверьте логи: `journalctl -u caddy -f` на сервере
- **Caddy не запускается**: `systemctl status caddy`

## Готовые файлы:
- `setup_vpn_domain.sh` — скрипт автоматизации (уже обновлён для pupupuuu.com)
- `quick_setup_guide.md` — эта инструкция

**Время выполнения**: 10-15 минут после добавления A-записи.