---
tags: [music-server, music, docker, lidarr, slskd, tubifarry]
created: 2026-06-04
status: ready
---

# T2: Lidarr + slskd + Tubifarry

## Что сделано

### Lidarr (порт 8686)
- Контейнер: `lscr.io/linuxserver/lidarr:latest`
- Данные: `/music/lidarr-config/`
- Музыка: `/music/library/` (общая)
- Статус: Up, REST API v3 работает
- API ключ: сгенерирован автоматически при первом запуске

### slskd (порт 5030)
- Контейнер: `slskd/slskd:latest`
- Данные: `/music/slskd-config/`
- Статус: Up, healthy
- Логин/пароль: сгенерированы автоматически — `slskd/slskd`
- Soulseek соединение: есть

### Tubifarry
- Скачан релиз v2.1.0: https://github.com/TypNull/Tubifarry
- Библиотека: `/music/lidarr-config/plugins/Tubifarry.dll`
- **Не активирован** — нужно через UI Lidarr добавить плагин

## Порты
| Сервис | Порт | Статус |
|--------|------|--------|
| Navidrome | 4533 | ✅ |
| Lidarr | 8686 | ✅ |
| slskd | 5030 | ✅ |

## Проверки
- slskd: healthy (healthcheck проходит)
- Lidarr: API v3 отвечает (требует key для полного доступа)
- Память: +~250MB (liddar ~130MB, slskd ~120MB)
- Диск: +~50MB конфигов
- Старые сервисы: не тронуты

## Требуется ручное действие
1. Зайти в Lidarr UI: http://77.73.135.110:8686
2. System → Plugins → вставить `https://github.com/TypNull/Tubifarry` → Install
3. Settings → Indexers → Add Slskd
4. Settings → Download Clients → Add Slskd

## Что дальше
- T3: Explo (рекомендации) — если нужно
- T4: Интеграция всех компонентов + тест загрузки одного трека
