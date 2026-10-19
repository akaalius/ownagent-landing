# OwnAgent landing

Лендинг для проверки спроса на услугу «личный ИИ-агент (Hermes / OpenClaw) на VPS клиента под ключ».
Статический сайт для GitHub Pages: RU на корне (`/`), EN в `/en/`, при первом заходе язык выбирается по браузеру.

## Структура
- `src/index.html` — шаблон (русский текст + плейсхолдеры)
- `src/i18n.en.json` — английские строки
- `build.py` — собирает `index.html`, `en/index.html`, `robots.txt`, `sitemap.xml`, `llms.txt` и JSON-LD (Service, Offer, FAQPage)
- `assets/` — favicon

Правки текста делать в `src/`, затем `python3 build.py`. Собранные файлы коммитятся, GitHub Pages отдаёт их как есть.

## Перед запуском
- `BASE_URL` в `build.py`: сменить на свой домен, пересобрать (canonical, hreflang, sitemap, llms.txt).
- Форма: заменить `REPLACE_ME` в `src/index.html` на id формы Formspree (formspree.io, бесплатно до 50 заявок в месяц), пересобрать.
- Счётчик: вставить код Яндекс Метрики или GoatCounter перед `</body>` в шаблоне; клики по CTA уже помечены `data-track`.
- После публикации: добавить сайт в Google Search Console и Яндекс Вебмастер, отправить `sitemap.xml`.

## Локально
`python3 -m http.server 8787` и открыть http://localhost:8787/ (RU) или http://localhost:8787/en/ (EN).
