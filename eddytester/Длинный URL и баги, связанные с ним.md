
Какой длинной может быть ссылка?
Есть ли вообще ограничение и какое?
пристегнись. Все довольно просто, но весть важные моменты о которых я не знал.

❗️По стандарту — можно хоть миллион символов в URL использовать

> 🧾 “HTTP does not place a pre-defined limit on the length of a URI”  
> — [RFC 7230 §3.1.1](https://datatracker.ietf.org/doc/html/rfc7230#section-3.1.1)

> “Interoperability depends on shared expectations of reasonable length”  
> — [RFC 7230 §2.7](https://datatracker.ietf.org/doc/html/rfc7230#section-2.7)

То есть в теории — безлимит.  

И логично, мы не знаем насколько сложной будет система параметров, попробуйте выбрать себе сложный тур агрегаторах, например.
У меня только выбор направления и дат уже занял 125 символов.

Но в реальности "безлимит" символов не такой уж резиновый и ломается на 2–4 тысячах символов.

⚙️ У каждого своё ограничение
Ограничения ссылок отсутствуют в стандарте, но есть в инструментах. Каждый браузер имеет свой лимит. И не только браузер.

Пара примеров с пруфами:

| Компонент       | Лимит (примерно) | Источник                                                                                                                                                |
| --------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **IE**          | 2 083 символа    | [Microsoft](https://support.microsoft.com/en-us/topic/maximum-url-length-is-2-083-characters-in-internet-explorer-174e7c8a-6666-f4e0-6fd6-908b53c12246) |
| **NGINX**       | 4 096            | [Docs](https://nginx.org/en/docs/http/ngx_http_core_module.html#large_client_header_buffers)                                                            |
| **Apache**      | 4 000            | [Docs](https://httpd.apache.org/docs/2.4/mod/core.html#limitrequestline)                                                                                |
| **AWS ALB**     | 8 192            | [AWS](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html)                                           |
| **Chrome / FF** | ~32 000          | [Sistrix](https://www.sistrix.com/ask-sistrix/technical-seo/site-structure/url-length-how-long-can-a-url-be)                                            |
| **Safari**      | до 80 000        | [StackOverflow](https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers)                                   |

🧨  Какие ошибки бывают?

- **414 URI Too Long** — URL не влез в лимит сервера или прокси
    
- **431 Request Header Fields Too Large** — особенно если куки раздуты
	URL (и query-параметры) — не считаются частью заголовков.
	
	Но: если query-параметры сериализуются в заголовки (в авторизации, куках, кастомных X-*), или если длина URL приводит к переполнению Referer, то косвенно это может вылиться в 431.
    
- **301 с обрезкой** — при фронтовом редиректе с огромными query-параметрами

🧵 _Реальный сценарий:_  
ты делаешь GET-запрос с фильтрами, кучей параметров, и всё вроде ок…  
но в ответ — `414 URI Too Long`. Или просто `400`. Или ничего.

> 🔍 Postman не всегда скажет прямо.  
> Может отдать “Bad Request” — но причина где-то в глубине сервера или прокси.

📚 [Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/414):

> “414 — сервер отказался обслуживать запрос, потому что URI слишком длинный.”

А [NGINX](https://nginx.org/en/docs/http/ngx_http_core_module.html#large_client_header_buffers) при превышении длины может **закрыть соединение без объяснений**.

🛡️ Безопасность: длинный URL — это уязвимость

> Recommended max: `2048` символов на URL, `1024` — на query string  
> — [RaiseUpWA](https://www.raiseupwa.com/writing-tips/what-is-the-limit-of-query-string-in-asp-net/)

📌 Почему?

- Это рекомендация от сканеров безопасности (Qualys, Acunetix)
    
- Огромный URL = потенциальная **Slow HTTP Request DoS атака**
    

🔐 В IIS даже рекомендуют это явно в `web.config`:

```xml
<requestLimits maxQueryString="1024" maxUrl="2048" />
```

💡 Так что длинный URL — это не просто неудобно. Это уязвимость.

---

## ✅ Что делать

- GET → только для коротких, понятных фильтров
    
- Сложные фильтры, массивы, Query DSL → **POST с телом запроса**
    
- Думай не только о браузере, но и о **прокси, CDN, сервере, API Gateway**
    


Подумываю собрать практикум, где такие штуки ловятся руками — без догадок на практике с реальным рабочим АПИ.  
Если хочешь попасть в тестовую волну — кинь + в коментах или пиши в личку. Добавлю. в тест-группу на запуске.

