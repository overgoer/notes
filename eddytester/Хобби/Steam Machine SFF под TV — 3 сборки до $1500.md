# Steam Machine SFF под TV — 3 сборки до $1500

**Дата:** Июнь 2025  
**Источники:** r/sffpc, PCPartPicker, SFF Network, bret.io, howtogeek.com, Digital Foundry, Optimum Tech  
**ОС:** Bazzite / ChimeraOS / SteamOS 3.7  
**GPU:** Только AMD Radeon  
**Сокет:** AM5  
**Форм-фактор:** Mini-ITX, <15L  
**Бюджет:** ~$1500 USD (актуальные цены США на июнь 2025)

---

## Сборка #1: «Console King» — Fractal Ridge + RX 7800 XT

**Корпус:** Fractal Design Ridge (12.6L, консольный, горизонтально/вертикально)  
**Концепция:** Идеальная Steam Machine под TV — размером с PS5, тихая, мощная.

### Компоненты

| Компонент | Модель | Цена (USD) |
|-----------|--------|-----------|
| **CPU** | AMD Ryzen 5 7600 (6C/12T, 65W) | $185 |
| **Кулер** | Thermalright AXP90-X47 Full Copper (47mm) | $25 |
| **Мат. плата** | ASRock B650I Lightning WiFi (AM5, WiFi/BT) | $170 |
| **RAM** | G.Skill Flare X5 32GB (2×16) DDR5-6000 CL30 | $95 |
| **SSD** | WD Black SN850X 2TB PCIe 4.0 NVMe | $130 |
| **GPU** | Sapphire Pulse Radeon RX 7800 XT 16GB (2.2 слота) | $470 |
| **Корпус** | Fractal Design Ridge PCIe 4.0 | $130 |
| **PSU** | Corsair SF750 (2024) 80+ Platinum SFX | $155 |
| **Вентиляторы** | 2× Noctua NF-A6x25 + 3× Arctic P8 Slim | $35 |
| **Хаб вентиляторов** | Noctua NA-FH1 | $15 |
| **Итого** | | **~$1410** |

### Clearance Validation
- **GPU длина:** Ridge поддерживает до 335 мм (325 мм с SSD в FX-L слоте). Sapphire Pulse RX 7800 XT: 250 мм ✅
- **GPU ширина:** 2.2 слота (43 мм) — влазит без проблем ✅
- **Кулер:** AXP90-X47 Full Copper — 47 мм, Ridge лимит CPU кулера 70 мм ✅
- **PSU:** SFX — Corsair SF750 идеально подходит, SFX-L не рекомендуется (толстые кабели) ✅

### Thermal Info
- CPU ~65°C под игровой нагрузкой (ECO mode 65W)
- GPU ~70-75°C, отличный приток через перфорированные панели
- Ryzen 5 7600 на 65W TDP хорошо охлаждается низкопрофильным кулером
- Рекомендуется: при установке под TV оставить 5-10 см зазора для выхлопа

### Сложность сборки: 6/10
Средняя сложность — много мелочей (кабель-менеджмент, замена вентиляторов, хаб). Но в целом корпус удобный.

### Комментарий
Проверенная временем сборка. Именно в таком корпусе собирает свою Steam Machine блогер Bret Comnes (bret.io). Bazzite работает «из коробки». Тихая, холодная, идеальна для гостиной.

---

## Сборка #2: «Sandwich Perfection» — Lian Li A4-H2O + RX 9070 XT

**Корпус:** Lian Li A4-H2O (11L, сэндвич-компоновка, 240mm AIO)  
**Концепция:** Максимум производительности на RDNA 4 в минимальном объёме.

### Компоненты

| Компонент | Модель | Цена (USD) |
|-----------|--------|-----------|
| **CPU** | AMD Ryzen 5 7600X (6C/12T, 105W) | $195 |
| **Кулер** | Cooler Master ML240L Core 240mm AIO | $65 |
| **Мат. плата** | ASRock B650I Lightning WiFi (AM5, WiFi/BT) | $170 |
| **RAM** | G.Skill Flare X5 32GB (2×16) DDR5-6000 CL30 | $95 |
| **SSD** | WD Black SN850X 2TB PCIe 4.0 NVMe | $130 |
| **GPU** | PowerColor Reaper Radeon RX 9070 XT 16GB (2-слот) | $600 |
| **Корпус** | Lian Li A4-H2O A4 PCIe 4.0 | $155 |
| **PSU** | Corsair SF750 (2024) 80+ Platinum SFX | $155 |
| **Итого** | | **~$1565** *(можно уложиться в $1500, выбрав RX 9070 non-XT ~$530)* |

### Clearance Validation
- **GPU длина:** A4-H2O поддерживает до 322 мм. PowerColor Reaper RX 9070 XT: ~280 мм ✅
- **GPU толщина:** до 3 слотов (60 мм). Reaper 2-слотовый ✅
- **AIO:** 240мм радиатор — обязателен для этого корпуса. ML240L влезает ✅
- **PSU:** SFX — Corsair SF750 идеально; SFX-L тоже влезает ✅

### Thermal Info
- AIO 240mm отлично справляется с 7600X (105W) — ~65°C в играх
- GPU ~70°C, отличная вентиляция через сэндвич-расположение
- Рекомендуется Undervolt GPU для снижения шума

### Сложность сборки: 7/10
Сэндвич-компоновка сложнее — требуется аккуратность с кабелями и AIO трубками. Но документация отличная, сообщество большое.

### Комментарий
Самая мощная сборка из трёх. RX 9070 XT даёт производительность уровня RTX 5070 Ti с 16GB VRAM. Если бюджет жмёт — берите RX 9070 (non-XT) (~$530), разница в цене ~$70, в производительности ~15%. Идеальна под 4K TV.

---

## Сборка #3: «Terra Compact» — Fractal Terra + RX 7800 XT

**Корпус:** Fractal Design Terra (10.4L, деревянная панель, регулируемый спин)  
**Концепция:** Эстетичный премиум-компакт для гостиной. Дорогой, красивый, продуманный.

### Компоненты

| Компонент | Модель | Цена (USD) |
|-----------|--------|-----------|
| **CPU** | AMD Ryzen 5 7600 (6C/12T, 65W) | $185 |
| **Кулер** | Noctua NH-L12S (70mm — в режиме CPU-focused) | $55 |
| **Мат. плата** | ASRock B650I Lightning WiFi (AM5, WiFi/BT) | $170 |
| **RAM** | G.Skill Flare X5 32GB (2×16) DDR5-6000 CL30 | $95 |
| **SSD** | WD Black SN850X 2TB PCIe 4.0 NVMe | $130 |
| **GPU** | ASRock Challenger Radeon RX 7800 XT 16GB (2.5 слота) | $470 |
| **Корпус** | Fractal Design Terra (Jade/Walnut) | $200 |
| **PSU** | Corsair SF750 (2024) 80+ Platinum SFX | $155 |
| **Итого** | | **~$1460** |

### Clearance Validation
- **Спин корпуса регулируемый (позиции 1-7):**
  - GPU ASRock Challenger RX 7800 XT: 2.5 слота (~50 мм ширина)
  - При 50 мм GPU → CPU cooler clearance = 72 - 50 = ~47 мм
  - **Проблема:** NH-L12S (70 мм) не влезет в этом режиме ❌
  - **Решение 1:** Перевести спин в CPU-focused режим (поз. 1): CPU до 70 мм, GPU ≤ 43 мм (2 слота). ASRock Challenger 2.5 слота не влезет ❌
  - **Решение 2:** Использовать AXP90-X47 Full (47 мм) + любую RX 7800 XT до 3 слотов ✅
  - **Рекомендуемый:** AXP90-X47 Full + PowerColor Fighter RX 7800 XT (2-слот) или Sapphire Pulse RX 7800 XT (2.2 слота) ✅
- **GPU длина:** Terra до 322 мм. Все компактные RX 7800 XT ~250-280 мм ✅

### Thermal Info (с AXP90-X47)
- CPU ~68-72°C под игровой нагрузкой (7600 65W)
- GPU ~72-78°C, отличный приток через сетчатые панели
- Noctua NH-L12S будет тише, но требует более тонкой GPU

### Сложность сборки: 5/10
Проще Ridge и A4-H2O. Открытый доступ ко всем сторонам, нет сэндвича. Но регулируемый спин добавляет головной боли при подборе.

### Комментарий
Самая красивая сборка. Terra с деревянной панелью выглядит как предмет мебели, а не как ПК. Однако компромиссы по clearance требуют внимательного подбора компонентов. Лучший вариант для гостиной, где важен внешний вид.

---

## Сводная таблица сравнения

| Параметр | #1 Console King | #2 Sandwich Perfection | #3 Terra Compact |
|----------|----------------|----------------------|-----------------|
| **Корпус** | Fractal Ridge | Lian Li A4-H2O | Fractal Terra |
| **Объём** | 12.6L | 11L | 10.4L |
| **CPU** | Ryzen 5 7600 | Ryzen 5 7600X | Ryzen 5 7600 |
| **GPU** | RX 7800 XT 16GB | RX 9070 XT 16GB | RX 7800 XT 16GB |
| **Охлаждение CPU** | Air (47mm) | 240mm AIO | Air (47mm) |
| **Стоимость** | ~$1410 | ~$1565 ($1500 с RX 9070) | ~$1460 |
| **FPS 1440p Ultra** | ~90-110 | ~120-140 | ~90-110 |
| **FPS 4K High** | ~55-70 | ~70-90 | ~55-70 |
| **Сложность сборки** | 6/10 | 7/10 | 5/10 |
| **Шум** | Тихий | Средний (AIO) | Тихий |
| **Clearance сложность** | Низкая | Средняя | Высокая (подбор) |
| **Эстетика** | Консоль | Стекло/алюминий | Дерево/алюминий |
| **Рекомендация** | 🏆 Лучшая для TV | 🚀 Самая мощная | 💎 Самая красивая |

---

## Российская действительность (июнь 2025)

Рекомендуемые площадки для поиска компонентов:
- **GPU:** Яндекс Маркет, DNS, Avito (б/у RX 7800 XT ~50-55 тыс. руб.)
- **Корпуса:** Fractal Ridge — редко, под заказ (~18-22 тыс. руб.). Fractal Terra — есть в DNS (~25 тыс. руб.)
- **CPU:** Ryzen 5 7600 — есть в DNS, Регард (~18-20 тыс. руб.)
- **PSU:** Corsair SF750 — редкость, можно Seasonic Focus SGX-650 SFX-L (~12-14 тыс. руб.)
- **Ориентировочный бюджет для РФ:** ~140-160 тыс. рублей (с учётом наценки)

---

## Советы по сборке

1. **Сначала Bazzite** — лучшая поддержка AMD. ChimeraOS — альтернатива. SteamOS 3.7 — если повезёт с железом
2. **Берите 2TB NVMe сразу** — 1TB на Steam Machine не хватит вообще
3. **Corsair SF750 — золотой стандарт** для SFF. Не экономьте на PSU
4. **Установка под TV:** Оставьте 5-10 см для вентиляции сзади. Fractal Ridge лучше всего ставить горизонтально
5. **WiFi/BT:** Все материнки в сборках имеют встроенный WiFi 6E/BT 5.3 — антенны в комплекте, но можно купить внешние магнитные для лучшего приёма
6. **Контроллеры:** Steam Controller, DualSense Edge или Xbox Wireless — все работают с Bazzite

---

## Источники

- [You can just build a Steam Machine — bret.io](https://bret.io/blog/2025/you-can-just-build-a-steam-machine/)
- [How-To Geek: Don't buy the Steam Machine, build one](https://www.howtogeek.com/dont-buy-the-steam-machine-build-a-pc-clone-instead/)
- [PCPartPicker — Fractal Ridge + RX 7800 XT builds](https://pcpartpicker.com/list/jjpqVF)
- [PCPartPicker — Lian Li A4-H2O + RX 7800 XT](https://pcpartpicker.com/b/JkZZxr)
- [Fractal Ridge build log — r/sffpc](https://www.reddit.com/r/sffpc/comments/17v2enh/fractal_ridge_build_log_and_guide_for_future/)
- [SFF.Network Fractal Ridge build guide](https://smallformfactor.net/news/l91-builds-fractal-ridge-gaming-sff-pc/)
- Tom's Hardware GPU Price Tracking — June 2025
