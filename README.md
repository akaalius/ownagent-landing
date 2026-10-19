# OwnAgent landing

Лендинг для проверки спроса на услугу «личный ИИ-агент (Hermes / OpenClaw) на VPS клиента под ключ».
Статическая страница, деплой на GitHub Pages. RU по умолчанию, EN через переключатель или `?lang=en`.

## Перед запуском
- Форма: заменить `REPLACE_ME` в `action` на id формы Formspree (formspree.io, бесплатно до 50 заявок в месяц).
- Счётчик: вставить код Яндекс Метрики или GoatCounter перед `</body>`; клики по CTA уже помечены `data-track`.
- Цены и контакты правятся прямо в `index.html` (секции `#price`, `#apply`, footer).

## Локально
Открыть `index.html` в браузере или `python3 -m http.server 8787`.
