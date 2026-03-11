# Clean Gutters Crew — PRD

## Original Problem Statement
Enhance and polish an existing cleaning service website (PHP/Twig) for cgc-services.ca.

## Core Requirements
1. **Performance Optimization (P0):** PageSpeed 90+ mobile/desktop
2. **Eliminate Regressions (P0):** Fix recurring UI bugs (burger menu, modals)
3. **UI/UX Polishing (P1):** Consistent, performant visuals
4. **SEO Improvement (P1):** Correct Schema.org structured data
5. **Maintain Functionality:** Forms, modals, navigation

## Tech Stack
- Backend: PHP, Twig
- Frontend: Vanilla JS, CSS, HTML
- No database
- External: Telegram API, Google reCAPTCHA, Facebook Pixel, Cloudflare

## What's Been Implemented

### Schema.org (COMPLETED)
- Main page: LocalBusiness + WebSite + WebPage + 6 Service entities
- FAQ page: WebPage + FAQPage with 14 Q&A items
- All 6 service pages: WebPage + BreadcrumbList(2-level) + Service
  - gutter_cleaning, window_washing, pressure_washing, moss_removal, junk_removal, handyman_services
  - All use consistent format: about=#business, areaServed=AdministrativeArea:Metro Vancouver

### Performance Tuning (COMPLETED)
- reCAPTCHA deferred until user interaction
- Hero images: loading="eager" + fetchpriority="high"
- FB Pixel delayed to 8000ms
- FontAwesome loaded via media="print" trick

### Bug Fixes (COMPLETED)
- Mobile burger menu: isolated to inline script in template.html.twig
- Areas modal: inline fallback + CSS fix
- Page jump fix: scrollRestoration='manual'
- Sticky button logic corrected
- Modal styling fixed for service pages
- Duplicate citiesModal removed from main.html.twig

### UI/UX (COMPLETED)
- Hero: 3 uniform buttons with pulsating animation
- Footer: social media icons (FB, WhatsApp, Instagram)
- Button styles standardized
- SEO text block on /quote page
- Navigation links reordered

## Pending Verification (USER)
1. Schema.org — test all service pages via Google Rich Results Test
2. Mobile burger menu — confirm working after hard refresh
3. PageSpeed score — retest service pages (target: 90+)

## Upcoming Tasks (P2)
- Unify Handyman page Title/H1 (inconsistent: "Repairs" vs "Services")
- Create dedicated /services page for 3-level breadcrumbs

## Future/Backlog (P2)
- Lightweight FAQ page template (no unnecessary modals/JS)
- FontAwesome optimization (load only needed icon sets)
- JS architecture refactor: consolidate app.js + page-city.js + inline scripts

## Code Architecture
```
/app/
├── public/
│   ├── assets/{css,js,images}/
│   └── index.php
├── resources/templates/
│   ├── template.html.twig (base: main page)
│   ├── page.html.twig (base: service pages)
│   ├── main.html.twig, faq.html.twig, quote.html.twig
│   ├── landing/services/ (6 service pages)
│   ├── landing/cities/ (17 city pages)
│   └── landing/components/header.html.twig
└── .env (TG_TOKEN, TG_CHANNEL)
```

## Key API Endpoints
- POST /quick-quote
- POST /applications
