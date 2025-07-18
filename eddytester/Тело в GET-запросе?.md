Все слышали этот вопрос на собеседовании:

«Можно ли отправить body в GET-запросе?»

Правильный ответ — можно, но не нужно. Никто и не отправляет.

Почти.

Недавно я натолкнулся на документацию, в которой явно указано, что НУЖНО отправлять запрос GET с телом. Речь об Elasticsearch — движке полнотекстового поиска и аналитики.

🚨 TL;DR

Да, технически тело в GET-запросе допустимо (см. RFC 2616).

Нет, это не рекомендуется использовать: большинство серверов игнорируют body в GET. Слова Express.js, Java Spring, Django вам о чем-нибудь говорят? Они не в курсе таких фокусов.

REST и OpenAPI НЕ ПОДДЕРЖИВАЮТ GET с body.

Elasticsearch делает это осознанно (и у них есть причина, ниже поясню)

Вывод для тестировщиков и разработчиков: вы обязаны знать, что такое возможно, и почему это рискованно.

🔍 Что говорит спецификация (RFC)

"A payload within a GET request message has no defined semantics" — RFC 7231, §4.3.1

То есть тело можно отправить, но оно не должно влиять на ответ. Это ставит под сомнение саму идею использования тела.
GET — для получения инфы, и никаких тел запроса.
Прямо так и написано в RFC 2616: "A message-body MUST NOT be included in a GET request." [1]

Почему это важно? У каждого HTTP-метода своя роль. GET — безопасный и идемпотентный.
То есть, дергай его хоть сто раз, ничего на сервере не изменится, только данные получишь. Многие клиенты, прокси и кэши просто игнорят тело в GET

**💡 А что делает Elasticsearch? (Спойлер: не от хорошей жизни)**

Elastic — та самая компания, которая создаёт Elasticsearch и Kibana — в документации прямо рекомендует GET с телом:

GET /my-index-000001/_search { "query": { "match": { "message": "this is a test" } } }

Это баг? Нет. Это фича. Это отклонение от стандарта, которое Elastic считает удобным. Почему? Все просто: Query DSL.
Это такой JSON-язык запросов, который позволяет творить с поиском чудеса. Сложные фильтры, агрегации, сортировки — все это пакуется в JSON.
И вот тут начинается самое интерес.

Представьте, что вам нужно найти что-то очень специфичное: "все статьи про Elasticsearch API, написанные в 2024 году, с упоминанием багов, и сгруппировать по авторам". Если это пихать в URL, получится монстр, который не пролезет ни в один браузер или прокси (там есть лимиты на длину URL, приложил в ссылках в полной версии статьи). А JSON-тело — это удобно, читаемо и масштабируемо.

И Elastic решил: пусть будет GET с телом, потому что семантически это все-таки получение данных, а не их изменение.
По смыслу, GET для поиска даже логичнее, чем POST.

Но этот "логичнее" вылез боком. Многие прокси и клиенты не в курсе таких тонкостей и просто ломаются. Поэтому сам Elastic теперь советует юзать POST для таких запросов. Логично? Ну, как сказать. Главное, что работает.

🔗 Пример из документации 🔗 Претензия на GitHub 🔗 Обсуждение в сообществе KNIME

⚠️ Почему это опасно?

Кэширование: Прокси и CDN могут кэшировать GET-запросы, игнорируя тело. Вы получите неверные данные. GET запросы должны кэшироваться. Это значит, что прокси или браузер может запомнить ответ и при следующем таком же запросе отдать его из своей памяти, не дергая Elastic. Быстро, удобно, нагрузка меньше. Но если в GET есть тело, кэш такой: "Эээ, это что за зверь?" И не кэширует. В итоге, каждый запрос, даже если он идентичен предыдущему, летит до самого Elastic. А это лишняя нагрузка, лишние задержки и, как следствие, тормоза. Особенно на больших объемах данных. Так что, за удобство платим производительностью.

Фреймворки: Многие серверы просто отбрасывают тело GET. Самый частый косяк — это когда между вашим приложением и Elasticsearch встает какой-нибудь прокси или балансировщик нагрузки. Например, AWS Application Load Balancer (ALB). Эти ребята — строгие. Они читают HTTP-спеку и говорят: "Тело в GET? Не положено!" И просто его выкидывают. В итоге, ваш запрос доходит до Elastic, но без Query DSL. А Elastic такой: "Эй, где мой JSON?" И выдает ошибку. Или, что еще хуже, возвращает все подряд, потому что фильтры потерялись.

REST и OpenAPI: Эти стандарты не поддерживают body в GET. Нельзя задокументировать корректно такие запросы. Другие поисковики и базы данных не стали изобретать велосипед: Apache Solr и MongoDB для сложных запросов используют POST с телом. Никаких сюрпризов.

Отладка: Postman, curl, Swagger — могут вести себя по-разному. Удачи найти баг. Попробуйте отладить GET с телом. Логи могут не показывать тело, инструменты типа Postman или curl могут вести себя по-разному. Ищи свищи, где зарыта собака. Время, нервы, деньги.
### Источники:

[1] RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1. Section 4.3 Message Body. [https://www.rfc-editor.org/rfc/rfc2616](https://www.rfc-editor.org/rfc/rfc2616) [2] Elasticsearch GET request with request body - curl - Stack Overflow. [https://stackoverflow.com/questions/36939748/elasticsearch-get-request-with-request-body](https://stackoverflow.com/questions/36939748/elasticsearch-get-request-with-request-body)