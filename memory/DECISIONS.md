# DECISIONS.md — Журнал согласованных решений

Этот файл ОБЯЗАТЕЛЕН к прочтению перед началом любой работы.
Каждое решение здесь — это согласованное с заказчиком правило. Не нарушать без явного разрешения.

---

## Рабочий процесс

- **ВСЕГДА:** Сначала анализ → потом план с оценкой → потом подтверждение от пользователя → потом работа
- Пользователь жаловался на то, что агент начинал работу без предварительного анализа. Это недопустимо.
- Пользователь технически грамотный, часто приносит готовые рекомендации от ChatGPT. Анализировать их серьёзно, но проверять.
- Язык общения: русский

### Обязательный анализ входящих рекомендаций
Когда пользователь присылает задание (своё или от ИИ), агент ОБЯЗАН перед выполнением:
1. Провести собственный анализ рекомендации
2. Чётко перечислить — что подтверждаю, что нет, и почему
3. Если есть сомнения — объяснить риски и предложить альтернативу
4. Получить подтверждение пользователя — только потом приступать к работе
Никогда не применять рекомендации вслепую, даже если они выглядят логично.

## Schema.org — Общие правила

- `LocalBusiness` — ТОЛЬКО на главной странице (`template.html.twig`)
- НЕ дублировать `LocalBusiness` на сервисных страницах
- НЕ добавлять `FAQPage` если на странице нет реального FAQ-блока
- `provider` на всех сервисных страницах ссылается на `{"@id": "https://cgc-services.ca/#business"}`
- Каждая service page должна иметь уникальные `url`, `name`, `description`, `@id`

## BreadcrumbList — Правила

- На сервисных страницах: строго **2 уровня** (Home → Service Name)
- НЕ добавлять промежуточный уровень "Services" пока нет отдельной страницы `/services`
- НЕ использовать якорные ссылки типа `https://cgc-services.ca/#services` в breadcrumbs — это не настоящая страница
- На `/quote`: 2 уровня (Home → Get a Quote)
- На `/faq`: breadcrumb не добавлен (можно добавить по запросу)

## Twig-архитектура (template.html.twig)

- Базовый шаблон содержит переопределяемые блоки:
  - `{% block page_title %}` — тег `<title>`
  - `{% block page_meta %}` — description, canonical, OG, Twitter
  - `{% block page_schema %}` — Schema.org JSON-LD
  - `{% block head_extra %}` — дополнительные элементы в `<head>`
  - `{% block styles %}`, `{% block content %}`, `{% block modals %}`, `{% block scripts %}`
- Дочерние шаблоны (quote, faq) переопределяют эти блоки для своих SEO-данных
- Главная страница (`main.html.twig`) наследует все дефолты — НЕ трогать дефолты без причины
- Сервисные страницы используют `page.html.twig` как базу (там свой `{% block schema %}`)

## Quote страница (/quote)

- Title: "Get a Free Quote in 1 Minute | Clean Gutters Crew"
- Canonical: `https://cgc-services.ca/quote`
- Schema: `ContactPage` + `BreadcrumbList` + `ContactPoint`
- Hero title: `<h1>`, НЕ `<div>` (было исправлено)

## FAQ страница (/faq)

- Title: "Frequently Asked Questions | Clean Gutters Crew"
- Canonical: `https://cgc-services.ca/faq`
- Schema: `WebPage` + `FAQPage`

## Сервисные страницы

- Все 6 страниц: `gutter_cleaning`, `window_washing`, `pressure_washing`, `moss_removal`, `junk_removal`, `handyman_services`
- Schema: `WebPage` + `BreadcrumbList`(2 уровня) + `Service`
- `areaServed`: `{"@type": "AdministrativeArea", "name": "Metro Vancouver"}` (НЕ перечислять города по отдельности)
- `about`: `{"@id": "https://cgc-services.ca/#business"}`

## Производительность (PageSpeed)

- Цель: 90+ mobile и desktop
- Facebook Pixel загружается с задержкой 8000мс
- reCAPTCHA загружается только при взаимодействии с формой (НЕ по таймеру)
- Hero images на service pages: `loading="eager"` + `fetchpriority="high"`
- FontAwesome: загружать ТОЛЬКО `solid.min.css` + `fontawesome.min.css` (НЕ `all.min.css`)
- `combined-city.min.css`: загружается через `preload` + `onload` (non-render-blocking)
- Critical CSS inline в `<style>` блоке `page.html.twig` — достаточно для above-fold рендера
- При изменении CSS: менять версию в query string (`?v=YYYYMMDDX`)

## JavaScript — Осторожно!

- JS архитектура ХРУПКАЯ: конфликты между `app.js`, `page-city.js` и inline-скриптами
- Бургер-меню — повторяющийся баг. Логика изолирована в inline-скрипт в `template.html.twig`
- При любых JS-изменениях — ВСЕГДА проверять бургер-меню на мобильном
- После минификации JS/CSS — проверять все страницы

## City Pages (17 штук)

- Title и H1 — НЕ МЕНЯТЬ. "Gutter Cleaning in [City]" это primary keyword, менять = потеря ранних SEO-позиций
- Schema шире чем title — это нормально. `serviceType` массив из 6 услуг, `Service.name` = "Exterior Cleaning Services in [City]"
- `about` → `#business` (не `#service`)
- Нет `offers` в schema
- BreadcrumbList: 2 уровня (Home → City Name)
- WebPage.description — ОБЯЗАТЕЛЬНО оставлять, с упоминанием других услуг
- Основной контент оставить (про gutter cleaning), НЕ переписывать
- Блок "Other Exterior Cleaning Services in [City]" с ссылками на service pages — добавлен
- Блок "Nearby Service Areas" с 5-6 соседних городов — добавлен (создаёт local SEO cluster)
- CTA блок с кнопкой Quote — добавлен
- Соседние города определены по географии Metro Vancouver, НЕ полный список из 17

## Известные нерешённые проблемы

- Title/H1 на handyman: Title="Handyman Repairs...", H1="Handyman Services" — несогласованность
- Нет отдельной страницы `/services` (нужна для 3-уровневых breadcrumbs)
- FAQ шаблон загружает лишние модалки и JS
- FontAwesome загружает всю библиотеку вместо нужных иконок
- JS требует рефакторинга: консолидация в один файл

---

*Обновлять после каждого согласования с заказчиком*
