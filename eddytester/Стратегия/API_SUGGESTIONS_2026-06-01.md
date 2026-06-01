# 🏗 API Improvement Suggestions — 2026-06-01

**Сгенерировано:** 2026-06-01 10:00
**Источник:** BSA API Bridge

---

## 1. File Upload Endpoint with Intentional Security Bugs

**Репозиторий:** free-trial-api
**Сложность:** P1

**Триггер:** 2026-05-17: Testing file uploads: multipart forms, validation, size limits, security (Zip Slip vulnerability)

**Описание:** Add a new POST /free/api/upload endpoint that accepts multipart file uploads. Intentionally introduce bugs: allow Zip Slip by not normalizing paths, accept oversized files, and allow arbitrary file types. This creates a realistic testing scenario for students.

**Стратегическая связь:** Training: provides hands-on security testing experience. Content: follow-up posts about how to detect and fix these bugs. Popularization: generates buzz around practical security testing.

**Контент-угол:** Follow-up post: 'I broke my own API with Zip Slip — here's how to find and fix it'

**Бриф для content_manager:**
> Title: 'Zip Slip in the Wild: Exploiting My Own API for Fun and Profit' | Angle: Show the vulnerable endpoint, demonstrate exploit, then walk through fixes (path normalization, size limits, file type validation) | Key points: curl example, code diff, security checklist

---

## 2. JWT Authentication for Protected Routes

**Репозиторий:** free-trial-api
**Сложность:** P1

**Триггер:** Backlog B-060: #post №3 VS Разработчик 21 401 Unauthorized - кто прав?

**Описание:** Add POST /free/api/auth/login endpoint that returns a JWT token, and require that token for existing GET /free/api/users and POST /free/api/users endpoints. Intentionally leave some endpoints unprotected for contrast. Include bugs like token expiration misconfiguration, missing validation, or exposing user data in token payload.

**Стратегическая связь:** Monetization: enables tiered access (trial vs paid tokens). Training: teaches authentication testing, token handling. Content: generates posts about 401 vs 403, token security, and common auth flaws.

**Контент-угол:** Post: 'The 401 Unauthorized mystery — why your token works sometimes but not others'

**Бриф для content_manager:**
> Title: 'Authentication Smackdown: Unpacking the 401 Error' | Angle: Compare correct and buggy implementations, show how to test auth flows with curl/Postman | Key points: token structure, validation logic, timing attacks, role-based access

---

## 3. User Stats Endpoint for Gamification and Analytics

**Репозиторий:** free-trial-api
**Сложность:** P2

**Триггер:** Strategic goal: increase engagement and content frequency (2-3 posts/week)

**Описание:** Add GET /free/api/users/stats endpoint that returns aggregated user data: total users, most active testers, bug discovery counts (if linked to bug database). Include intentional data leakage bug (e.g., returning emails without pagination).

**Стратегическая связь:** Popularization: gamifies learning, encourages sharing results. Content: sparks discussions about data privacy and analytics. Training: teaches aggregation queries, rate limiting, and data exposure risks.

**Контент-угол:** Post: 'I accidentally exposed all user emails — here's what I learned about API analytics'

**Бриф для content_manager:**
> Title: 'Analytics Gone Wrong: How My Stats Endpoint Leaked User Data' | Angle: Build the endpoint, show the bug, fix with pagination and access control | Key points: SQL aggregation, response design, security audit

---

> Статус: предложено → принято/отклонено → сделано → опубликовано
> Отмечай статус в API_IMPROVEMENT_TRACKER.md