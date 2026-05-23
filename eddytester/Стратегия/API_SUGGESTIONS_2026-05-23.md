# 🏗 API Improvement Suggestions — 2026-05-23

**Сгенерировано:** 2026-05-23 03:01
**Источник:** BSA API Bridge

---

## 1. File Upload Endpoint with Security Demonstrations

**Репозиторий:** v0-test-api
**Сложность:** P1

**Триггер:** 2026-05-17 post about Zip Slip and file upload security

**Описание:** Add a POST /uploads endpoint that accepts file uploads (multipart form) with validation: file size limit, allowed extensions, and path traversal protection. Include intentional bugs like missing path sanitization to demonstrate Zip Slip vulnerability.

**Стратегическая связь:** Provides a real-world example for security testing content, attracts students interested in API security, and can be gated (premium feature) for monetization.

**Контент-угол:** Build a vulnerable file upload endpoint and teach how to test and fix it

**Бриф для content_manager:**
> Title: 'How to Build (and Break) a File Upload API in Node.js' — Walk through creating the endpoint, then show how Zip Slip works, and finally fix it. Publish as a series or tutorial.

---

## 2. Strict Content-Type Validation Middleware

**Репозиторий:** v0-test-api
**Сложность:** P1

**Триггер:** Backlog post B-057: 'Content-Type text/plain on JSON endpoint'

**Описание:** Add middleware that checks Content-Type header on POST/PUT endpoints expecting JSON. Return 415 Unsupported Media Type with proper error message if wrong. Include optional bypass for testing (e.g., header x-test-bypass: true).

**Стратегическая связь:** Teaches API design best practices, provides a simple but valuable bug to showcase, and can be used in educational content about RESTful API standards.

**Контент-угол:** Why Content-Type matters and how to enforce it properly

**Бриф для content_manager:**
> Title: 'API Blunder #10: Accepting Any Content-Type' — Show an API that silently parses text/plain as JSON, then implement proper validation. Encourage readers to test their own APIs.

---

## 3. Free Trial API: Add Usage Tracking and Balance Endpoint

**Репозиторий:** free-trial-api
**Сложность:** P0

**Триггер:** Backlog: B-001 (fix Free Trial API) and B-004 (trial to payment flow)

**Описание:** After fixing authentication, add GET /free/api/balance to return remaining requests or credits. Track usage per API key in a simple in-memory or SQLite store. Include a reset endpoint for admin.

**Стратегическая связь:** Directly supports monetization by showing users their trial limit, encourages upgrade, and provides a clear API demo for the channel (e.g., 'See how usage-based billing works').

**Контент-угол:** Implementing usage tracking for a freemium API

**Бриф для content_manager:**
> Title: 'Building a Usage-Based API: From Free Trial to Paid Plan' — Show how to add a balance endpoint, track requests, and trigger upgrade prompts. Use this as a case study for monetization.

---

> Статус: предложено → принято/отклонено → сделано → опубликовано
> Отмечай статус в API_IMPROVEMENT_TRACKER.md