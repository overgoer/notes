# 🏗 API Improvement Suggestions — 2026-05-21

**Сгенерировано:** 2026-05-21 22:03
**Источник:** BSA API Bridge

---

## 1. Implement secure file upload endpoint

**Репозиторий:** free-trial-api
**Сложность:** P1

**Триггер:** 2026-05-17: Testing file uploads: multipart forms, validation, size limits, security

**Описание:** Add POST /free/api/upload endpoint that accepts multipart file uploads, validates file type and size, and implements zip-slip prevention (path traversal checks, symbolic link removal). Store files in a sandboxed directory with randomized names.

**Стратегическая связь:** Teaches real-world security practices; provides content for a step-by-step bug fix post; attracts learners interested in API security.

**Контент-угол:** Post: 'How I built a secure file upload API in 2 hours (and how you can break it)' — demo the endpoint, show zip-slip exploitation, then reveal the fix.

**Бриф для content_manager:**
> Title: Secure File Upload in Practice – Zip Slip Demo & Fix. Angle: Follow-along implementation with security pitfalls. Key points: multipart parsing, validation, path traversal prevention, symlink removal, sandboxing.

---

## 2. Fix Free Trial API auth and add payment endpoint

**Репозиторий:** free-trial-api
**Сложность:** P0

**Триггер:** Backlog B-001: Free Trial API broken auth; B-004: payment flow needed

**Описание:** Repair PostgreSQL authentication and /free/api/users endpoint (currently 404). Add POST /free/api/payment/create to generate a payment link (e.g., Telegram Stars or YooKassa) for full access. Return a payment URL and handle webhook for confirmation.

**Стратегическая связь:** Directly enables monetization; unblocks the entire free trial funnel; generates content about fixing a broken API and integrating payments.

**Контент-угол:** Post: 'Turning a broken API into a payment gateway' — walk through debugging auth issues, then adding a simple payment flow. Shows real problem-solving and monetization.

**Бриф для content_manager:**
> Title: From 404 to Payment: Fixing and Expanding Free Trial API. Angle: Real debugging journey. Key points: auth fix, endpoint creation, payment integration, webhook handling, testing the complete flow.

---

## 3. Add bug-report challenge endpoint

**Репозиторий:** v0-test-api
**Сложность:** P2

**Триггер:** Backlog B-059: #post №4 Угадай баг 16 (quiz format); strategy: interactive learning

**Описание:** Add POST /challenges/submit that accepts a bug report (user's analysis). Also add GET /challenges/:id/feedback that returns automated feedback comparing user's answer with known bugs. Store submissions in DB for analytics.

**Стратегическая связь:** Turns passive content into interactive learning; builds community engagement; provides data for future content and personalized learning paths.

**Контент-угол:** Post: 'I created an API that teaches you to find bugs — try it!' — launch the challenge endpoint, show how it works, and invite followers to submit their findings. Then follow up with results.

**Бриф для content_manager:**
> Title: Learn API Bug Hunting with This Interactive Challenge. Angle: Gamified learning. Key points: submission endpoint, automated feedback, leaderboard potential, integration with existing quiz posts.

---

> Статус: предложено → принято/отклонено → сделано → опубликовано
> Отмечай статус в API_IMPROVEMENT_TRACKER.md