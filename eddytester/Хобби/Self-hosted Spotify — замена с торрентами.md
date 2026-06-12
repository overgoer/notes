# Self-hosted Spotify — замена с торрентами и рекомендациями

> **Цель:** полностью автономный музыкальный стриминг без подписок, с рекомендациями как в Spotify. Всё своё, без блокировок.
> 
> **Важно:** только музыка. Не видео, не кино.

---

## Стеки в 2026 году

Сейчас сложились 2 основных стека. Выбирай по вкусу.

### Стек A: Navidrome + Lidarr + Tubifarry + Soulseek

**Философия:** лёгкий, только музыка, opensource, без Plex Pass

```
Navidrome (стриминг) ←— Lidarr (менеджер библиотеки) ←— Tubifarry (плагин)
                                      ↓
                                slskd (Soulseek)
                                      ↓
                            P2P-сеть Soulseek
```

| Компонент | Роль | Ссылка |
|-----------|------|--------|
| **Navidrome** | Лёгкий стриминговый сервер (Go). Жрёт копейки. Subsonic API. | github.com/navidrome/navidrome |
| **Lidarr** | Менеджер коллекции. Следит за артистами, ищет альбомы, сортирует. | lidarr.audio |
| **Tubifarry** | **Плагин к Lidarr** (2025-2026). Добавляет: Soulseek как источник, YouTube как источник, автоимпорт Spotify-плейлистов. | github.com/TypNull/Tubifarry |
| **slskd** | Headless Soulseek-клиент (веб-интерфейс, API). | github.com/slskd/slskd |
| **Prowlarr** | (опционально) Индексатор торрентов, если хочешь и торренты. | prowlarr.com |

**iOS-клиенты для Navidrome:**
- **Symphonium** ($6) — лучший. CarPlay, офлайн, красиво
- **play:Sub** ($5) — Subsonic-клиент, работает
- **Sonixd / Feishin** — десктопные (Electron)

### Стек B: Plex + Lidarr + Soulseek + Plex Amp

**Философия:** тяжелее, но Plex Amp — arguably лучший музыкальный клиент вообще

```
Plex (стриминг + библиотека) ←— Lidarr
       ↓
Plex Amp (iOS/Android/CarPlay)
```

- **Plex Amp** — охуенный клиент. CarPlay, офлайн, умные плейлисты, тексты, рекомендации. Но: нужен Plex Pass ($5/мес или $120 lifetime).
- Plex как платформа в 2025-2026 **пошёл по пути монетизации** — paywall на удалённый стриминг своей же библиотеки. Комьюнити злится.
- Сама экосистема Plex тяжелее Navidrome. Это медиа-сервер для всего, а не только музыка.

---

## Скачивание музыки — ключевые источники

### Soulseek (slskd) — главный рекомендованный

- P2P-сеть, существует 20+ лет. Специализируется на музыке.
- **Отличие от торрентов:** не трекеры, нет «роя». Просто люди ша́рят папки. Никто не отслеживает.
- **Безопасность:** DMCA-уведомления приходят на трекеры, а не на Soulseek. Редитор: "25 years on slsk, zero issues with ISP." 
- **Как не получить бан:** шарить свою библиотеку обратно (100+ файлов), не скачивать от пользователей с фейковыми файлами, не флудить запросами.
- **slskd** — headless версия для сервера. Ставится в Docker, имеет API для интеграции с Lidarr.

### Tubifarry (YouTube как источник)

- Tubifarry умеет качать с YouTube как fallback
- Если Soulseek не нашёл — тянет с YouTube, конвертирует, чистит теги
- Аудио с YouTube — не lossless, но для фонового прослушивания норм

### Torrents (через Prowlarr + qBittorrent/Transmission)

- Классические торренты для музыки — REDacted, Orpheus, DeeJayDam. Но: нужен инвайт.
- Публичные трекеры — риск DMCA (если провайдер следит). На Амстердаме — aeza может получить жалобу.
- **Не рекомендую для музыки.** Soulseek надёжнее и безопаснее.

### Deemix / SpotiDown / Downtify — НЕ РЕКОМЕНДУЮ

- Качают напрямую со Spotify. Spotify активно давит — были C&D письма (Spotube).
- Deemix давно мёртв, форки нестабильны
- Качество — 128-160kbps Ogg, не lossless
- Юридически серая зона (нарушение ToS), в Европе за это штрафуют
- **Риск:** бан аккаунта Spotify, если используется твой аккаунт

---

## Рекомендации — самая важная часть

### Explo — то что нужно (лучшее)

**github.com/LumePart/Explo**

Это self-hosted аналог **Discover Weekly** от Spotify. Работает так:
1. Ты слушаешь музыку через Navidrome
2. Navidrome отправляет историю прослушиваний в ListenBrainz (scrobbling)
3. Explo забирает рекомендации из ListenBrainz
4. Explo качает рекомендованные треки (через настроенный downloader — Soulseek/torrent)
5. Музыка попадает в твою библиотеку

По сути — **замкнутый цикл:** слушаешь → рекомендации → скачивание → слушаешь.

**Не требует:** API ключей Spotify, подписок, аккаунтов в стримингах.
**Всё open source.** Написано на Python, ставится легко.

### ListenBrainz (бесплатно)

- Open source база данных listening history. Как Last.fm, но open.
- Бесплатный API для рекомендаций
- Explo использует именно его

### Navidrome + плагин ListenBrainz

- Navidrome умеет сам отправлять scrobbles в ListenBrainz (встроенный плагин)
- И сам генерировать рекомендации на основе LB

### Mixarr (для продвинутых)

**github.com/aquantumofdonuts/mixarr** — музыкальный discovery-компаньон для Lidarr. Подключается к Spotify, Tidal, Deezer, Bandcamp, Discogs — ищет похожую музыку, рекомендует артистов. Но: требует API ключи стримингов.

---

## Безопасность — чтобы не поймали

| Действие | Риск | Решение |
|----------|------|---------|
| Торренты без VPN | DMCA-жалоба провайдеру | Не использовать торренты для музыки вообще |
| Soulseek | Низкий (нет трекеров, P2P напрямую) | slskd сам не светится. Шарить библиотеку — обязательно |
| YouTube (Tubifarry) | Нулевой — ты просто смотришь ютуб | Норм |
| Deemix / Spotify ripping | Средний — Spotify банит аккаунты | Не использовать |

**На Амстердаме (aeza):**
- Soulseek через Docker — безопасно
- Торренты — **только через VPN** (Mullvad / Proton VPN / AirVPN). **Без VPN нельзя** — aeza может отключить сервер по DMCA
- Tubifarry (YouTube) — без риска

---

## Финальная рекомендация

### **Navidrome + Lidarr + Tubifarry (slskd) + Explo**

**Почему этот стек:**

| Пункт | Почему |
|-------|--------|
| Полностью open source | Никаких Plex Pass, никаких подписок |
| Лёгкий | Navidrome в Go — 20MB RAM. Влезет на любой сервер |
| Автоматические рекомендации | Explo делает Discover Weekly для твоей библиотеки |
| Безопасный | Soulseek — нет DMCA. Никто не придёт |
| Под iPhone | Symphonium / play:Sub — хорошие iOS-клиенты |
| Не требует VPN | Soulseek и YouTube не светятся |

**Что не входит:**
- Lossless-качество (FLAC) — Soulseek есть, но не гарантированно
- Идеальный iOS-клиент как Plex Amp — Symphonium близко, но не идеал

**Если хочешь максимально красивый клиент любой ценой:**

Plex + Plex Amp — интерфейс топ. Но Plex Pass стоит денег, а сама платформа всё больше монетизируется.

---

## План развёртывания (если решим делать)

### Фаза 1 — База

- [ ] Запустить Navidrome в Docker на Амстердаме
- [ ] Создать каталог `/music/library`
- [ ] Закинуть пару альбомов вручную — проверить стриминг через Symphonium на iPhone

### Фаза 2 — Автоматизация загрузок

- [ ] Запустить slskd в Docker
- [ ] Настроить Lidarr (Docker), привязать к slskd как downloader
- [ ] Установить плагин Tubifarry в Lidarr
- [ ] Добавить первых артистов в Lidarr — проверить, что скачивается и импортируется

### Фаза 3 — Рекомендации

- [ ] Зарегистрироваться в ListenBrainz
- [ ] Подключить Navidrome scrobbling → ListenBrainz
- [ ] Запустить Explo
- [ ] Настроить Explo → скачивание рекомендованного
- [ ] Проверить недельный цикл: слушаешь → пятница → новые треки в библиотеке

---

## Ссылки

| Ресурс | Ссылка |
|--------|--------|
| Navidrome | github.com/navidrome/navidrome |
| Lidarr | lidarr.audio |
| Tubifarry | github.com/TypNull/Tubifarry |
| slskd | github.com/slskd/slskd |
| Explo | github.com/LumePart/Explo |
| ListenBrainz | listenbrainz.org |
| Symphonium (iOS) | symphonium.app |
| play:Sub (iOS) | App Store |
| Обзор стека (Reddit 2025) | reddit.com/r/selfhosted/comments/1qhnmv8 |
| Настройка Navidrome + LB | chhs1.github.io/blog/2026/01/22/self-hosted-discovery-playlists |
| Отдельный гайд (Tubifarry + Lidarr + slskd) | raw.githubusercontent.com/TypNull/Tubifarry/master/README.md |
