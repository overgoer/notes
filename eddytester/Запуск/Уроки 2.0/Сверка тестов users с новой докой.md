# Сверка практических тестов users с новой докой

> Проверено вживую против v1 (24.08) + новая дока (0–17 minor, 18–65 candidate, 66+ retired, без верхней границы).
> v1-баги не трогаем — правим только ТЕСТЫ (LESSONS_CONFIG) под актуальную доку.

---

## POST /users (post-users)

| Пункт | В тесте | Факт v1 | Вердикт |
|---|---|---|---|
| p_name_special «цифры/символы проходят» | correct | принимает | ✅ баг, ок |
| p_age_66 «66+ отклоняется» | correct | 400 «17 and 65» | ✅ баг, ок (дока: 66+ retired валиден) |
| p_age_string «возраст строкой» | correct | `"age":"17"` | ✅ баг, ок |
| p_passes «2 пропуска» | correct | 2 пропуска | ✅ баг, ок |
| p_status_17 «17 → minor (должен candidate)» | correct | 17 → **candidate** | ❌ формулировка ПЕРЕВЁРНУТА: v1 даёт candidate, дока требует minor. Текст: «17 → candidate (должен быть minor)» |
| p_age_17 «17 проходит (граница 18)» | дистрактор | 17 проходит (валидно по доке) | ⚠️ формулировка устарела («граница 18» — неправда). Заменить или убрать |
| p_empty_body «пустое → 200» | дистрактор | 400 | ✅ не баг, ок |
| p_name_trim / p_name_length / p_extra_field | дистракторы | — | ✅ ок (дока не описывает) |
| **НОВЫЙ: «возраст младше 17 отклоняется (например, 10)** | — | 400 «17 and 65» | ❗ добавить в correct (дока: 0–17 minor валиден) |

## GET /users/:id (get-user)

| Пункт | В тесте | Факт v1 | Вердикт |
|---|---|---|---|
| u_id_minus «id=2 → id=1» | correct | запрос 158 → вернул 157 | ✅ баг, ок |
| u_not_found «200 {} вместо 404» | correct | 404 (и на чистой базе) | ❌ НЕ баг — убрать из correct |
| u_string_id «abc → 500» | correct | 500 «Server error» | ✅ баг, ок |
| u_no_id_trap «нет id» | дистрактор | id есть | ✅ не баг, ок |
| u_pagination / u_no_total_count / u_cache_private | дистракторы | — | ✅ ок (дока не описывает) |

## PATCH /users/:id (patch-user)

| Пункт | В тесте | Факт v1 | Вердикт |
|---|---|---|---|
| h_age_negative «−5 → 500» | correct | 500 «Server error» | ✅ баг, ок |
| h_no_id «нет id в ответе» | correct | ответ без id | ✅ баг, ок |
| h_age_string «возраст строкой» | correct | `"age":"30"` | ✅ баг, ок |
| h_name_special «имя без валидации» | correct | PATCH «Name123» → 200 | ✅ баг, ок |
| h_no_status_retired «нет status при 66+» | correct | PATCH 66 → 200, ответ БЕЗ status | ✅ баг, ок |
| h_partial_update «name сбрасывает age» | дистрактор | age НЕ сбрасывается | ✅ не баг, ок |
| h_empty_body / h_extra_field / h_empty_name | дистракторы | 400 | ✅ не баги, ок |
| h_age_high «>65 не отклоняется» | дистрактор | v1 отклоняет | ✅ дистрактор ок (но по новой доке отклонение 66+ — БАГ, уже есть p_age_66 в POST; в PATCH — см. выше) |

## DELETE /users/:id (delete-user)

| Пункт | В тесте | Факт v1 | Вердикт |
|---|---|---|---|
| d_wrong_code «200 вместо 204» | correct | 200 | ❌ дока НЕ требует 204 (пример ответа без кода; v2 — 200). Убрать из correct |
| d_no_key_filter «любой ключ» | correct | чужой ключ → 200 «deleted» | ✅ баг, ок |
| d_cleanup «GET возвращает после удаления» | correct | SELECT вместо DELETE | ✅ баг, ок |
| d_not_found «несуществующий → 200» | **дистрактор** | 200 «deleted successfully» | ❗ это БАГ (дока: 404) — перевести в correct |
| **НОВЫЙ: «в ответе нет удалённого user»** | — | только message | ❗ добавить в correct (дока: {message, user}) |
| d_negative_id / d_string_id | дистракторы | — | ✅ ок (дока явно не описывает) |

## GET /users (get-users) — без изменений

Все 7 correct подтверждены, дистракторы ок. Спорный: g_cache_info «X-Cache-Info утекает» — дока заголовок не упоминает, но утечка реальная — оставляем (вопрос Эдди при желании).

---

## Итого правок в LESSONS_CONFIG

1. post-users: перевернуть формулировку p_status_17; убрать/заменить p_age_17; **добавить баг «младше 17 отклоняется»**
2. get-user: убрать u_not_found из correct (или перепроверить); проверить u_string_id
3. patch-user: проверить h_name_special, h_no_status_retired вживую
4. delete-user: убрать d_wrong_code из correct; **перевести d_not_found в correct**; **добавить «нет user в ответе»**

Все ⏳ закрыты проверками 24.08: u_string_id ✓ баг, h_name_special ✓ баг, h_no_status_retired ✓ баг (PATCH 66 → ответ без status), d_no_key_filter ✓ баг (чужой ключ удаляет).
