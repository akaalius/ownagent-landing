#!/usr/bin/env python3
"""Собирает index.html (RU) и en/index.html (EN) из src/index.html + src/i18n.en.json,
плюс robots.txt, sitemap.xml, llms.txt. Запуск: python3 build.py"""
import json, re, html, pathlib, datetime

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://getownagent.com"   # сменить на свой домен без слеша в конце
GA_ID = "G-VWBSFKVFRQ"   # Google Analytics 4 Measurement ID вида G-XXXXXXXXXX; пусто = без счётчика
CLARITY_ID = "z0j86ikxxd"   # Microsoft Clarity project id; пусто = выключено
METRIKA_ID = "113690948"   # Яндекс Метрика, номер счётчика; пусто = выключено
TPL = (ROOT / "src/index.html").read_text(encoding="utf-8")
EN = json.loads((ROOT / "src/i18n.en.json").read_text(encoding="utf-8"))
HTML_KEYS = {"ap.alt", "term.body"} | {"inc.f%d" % i for i in range(1, 15)}

META = {
  "ru": dict(lang="ru", title="OwnAgent: личный ИИ-агент в Telegram, на вашем сервере",
             desc="Личный ИИ-агент Hermes или OpenClaw в Telegram на вашем сервере. Ставим, настраиваем и закрываем от чужих, терминал не нужен. 9 900 ₽, готово за день, отчёт по 14 проверкам.",
             og_desc="Установка под ключ с защитой. Данные остаются у вас.", locale="ru_RU", path="/", assets="assets/",
             ru_href="./", en_href="en/"),
  "en": dict(lang="en", title="OwnAgent: your AI agent in Telegram, on your own server",
             desc="Your personal AI agent (Hermes or OpenClaw) in Telegram, on your own server. We install, configure and lock it down, no terminal needed. $99, done in a day, report on 14 checks.",
             og_desc="Turnkey, hardened install. Your data stays on your server.", locale="en_US", path="/en/", assets="../assets/",
             ru_href="../", en_href="./"),
}

def replace_i18n(src, key, value):
    """Заменить innerHTML у всех элементов с data-i18n=key, учитывая вложенные теги того же имени."""
    pos = 0
    while True:
        m = re.search(r'<([a-z0-9]+)([^>]*?)\sdata-i18n="%s"([^>]*)>' % re.escape(key), src[pos:])
        if not m:
            return src
        tag = m.group(1); start = pos + m.end()
        depth = 1; i = start
        pat = re.compile(r'<(/?)%s\b[^>]*>' % tag)
        while depth:
            mm = pat.search(src, i)
            if not mm: raise ValueError("unclosed " + key)
            depth += -1 if mm.group(1) else 1
            i = mm.end() if depth else mm.start()
        src = src[:start] + value + src[i:]
        pos = start + len(value)

EN_ATTRS = {
    'aria-label="Пример вывода установщика"': 'aria-label="Installer output, example"',
    'placeholder="@telegram или email"': 'placeholder="@telegram or email"',
}

def faq_jsonld(page):
    qs = re.findall(r'<summary[^>]*>(.*?)</summary><div class="a"[^>]*>(.*?)</div>', page, re.S)
    strip = lambda t: html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qs]}

def service_jsonld(lang):
    ru = lang == "ru"
    return {"@context": "https://schema.org", "@type": "Service",
            "name": "OwnAgent", "serviceType": "AI agent deployment on client VPS" if not ru else "Развёртывание ИИ-агента на VPS клиента",
            "description": META[lang]["desc"], "url": BASE_URL + META[lang]["path"], "areaServed": "Worldwide",
            "provider": {"@type": "Organization", "name": "OwnAgent", "email": "aka.alius@gmail.com", "url": BASE_URL + "/",
                         "sameAs": ["https://t.me/pasee2"]},
            "offers": [
              {"@type": "Offer", "name": "Personal (launch price, first 20 installs)", "price": "9900" if ru else "99", "priceCurrency": "RUB" if ru else "USD", "url": BASE_URL + META[lang]["path"] + "#price",
               "description": "Hermes Agent or OpenClaw on your VPS, hardened, Telegram, spending cap, backups, monitoring, 14-check report, 14 days of support" if not ru else
                              "Hermes Agent или OpenClaw на вашем VPS с защитой, Telegram, лимит расходов, бэкапы, мониторинг, отчёт по 14 проверкам, 14 дней поддержки"},
              {"@type": "Offer", "name": "Business", "price": "39000" if ru else "390", "priceCurrency": "RUB" if ru else "USD", "url": BASE_URL + META[lang]["path"] + "#price",
               "description": "Personal plus two integrations, express security audit, setup call, 30 days of support" if not ru else
                              "Personal плюс две интеграции, экспресс-аудит безопасности, созвон по настройке, 30 дней поддержки"}
            ]}

def analytics_html():
    analytics = ""
    if GA_ID:
        analytics = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
                     '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","%s");</script>') % (GA_ID, GA_ID)
    if CLARITY_ID:
        analytics += ('\n<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
                      't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})'
                      '(window, document, "clarity", "script", "%s");</script>') % CLARITY_ID
    if METRIKA_ID:
        analytics += ('\n<script>(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();'
                      'for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}'
                      'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
                      '(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id=%s","ym");'
                      'ym(%s,"init",{ssr:true,webvisor:true,clickmap:true,referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});</script>'
                      '\n<noscript><div><img src="https://mc.yandex.ru/watch/%s" style="position:absolute;left:-9999px" alt=""></div></noscript>') % ((METRIKA_ID,) * 3)
    return analytics

def build(lang):
    m = META[lang]; page = TPL
    if lang == "en":
        for k, v in EN.items():
            if k.endswith("ph"): continue
            page = replace_i18n(page, k, v)
        for a, b in EN_ATTRS.items():
            page = page.replace(a, b)
    canonical = BASE_URL + m["path"]
    head = "\n  ".join([
        f'<link rel="canonical" href="{canonical}">',
        f'<link rel="alternate" hreflang="ru" href="{BASE_URL}/">',
        f'<link rel="alternate" hreflang="en" href="{BASE_URL}/en/">',
        f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}/en/">',
        '<script type="application/ld+json">' + json.dumps(service_jsonld(lang), ensure_ascii=False) + '</script>',
        '<script type="application/ld+json">' + json.dumps(faq_jsonld(page), ensure_ascii=False) + '</script>',
    ])
    page = (page.replace("__HEAD_SEO__", head).replace("__ASSETS__", m["assets"]).replace("__LANG__", m["lang"])
                .replace("__TITLE__", m["title"]).replace("__OG_TITLE__", m["title"]).replace("__META_DESC__", m["desc"])
                .replace("__OG_DESC__", m["og_desc"]).replace("__OG_IMAGE__", BASE_URL + "/assets/og-" + lang + ".png").replace("__CANONICAL__", canonical).replace("__OG_LOCALE__", m["locale"])
                .replace("__RU_HREF__", m["ru_href"]).replace("__EN_HREF__", m["en_href"])
                .replace("__RU_CUR__", 'aria-current="page"' if lang == "ru" else "").replace("__EN_CUR__", 'aria-current="page"' if lang == "en" else ""))
    analytics = analytics_html()
    page = page.replace("__ANALYTICS__", analytics)
    page = page.replace(' >', '>')
    assert "__" not in re.sub(r"__(?:proto)", "", page.replace("--", "")), "unfilled placeholder"
    out = ROOT / ("index.html" if lang == "ru" else "en/index.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out

# Подстраницы: шаблон src/<name>.html, перевод src/i18n.<name>.en.json, адреса /<name>/ и /en/<name>/
SUBPAGES = {
  "report": {
    "ru": dict(title="Пример отчёта OwnAgent: 14 проверок после установки",
               desc="Пример формата отчёта OwnAgent: 14 проверок безопасности и надёжности и артефакт по каждой. Значения условные."),
    "en": dict(title="OwnAgent sample report: 14 checks after install",
               desc="Sample OwnAgent report format: 14 security and reliability checks with the artifact for each. Placeholder values."),
  },
  "privacy": {
    "ru": dict(title="Политика конфиденциальности OwnAgent",
               desc="Какие данные получает сайт getownagent.com, зачем, где они обрабатываются, сколько хранятся и как их удалить."),
    "en": dict(title="OwnAgent privacy policy",
               desc="What data getownagent.com receives, why, where it is processed, how long it is kept and how to have it deleted."),
  },
}

def build_subpage(name, lang):
    m = SUBPAGES[name][lang]
    page = (ROOT / f"src/{name}.html").read_text(encoding="utf-8")
    if lang == "en":
        for k, v in json.loads((ROOT / f"src/i18n.{name}.en.json").read_text(encoding="utf-8")).items():
            page = replace_i18n(page, k, v)
    path = f"/{name}/" if lang == "ru" else f"/en/{name}/"
    canonical = BASE_URL + path
    head = "\n  ".join([
        f'<link rel="canonical" href="{canonical}">',
        f'<link rel="alternate" hreflang="ru" href="{BASE_URL}/{name}/">',
        f'<link rel="alternate" hreflang="en" href="{BASE_URL}/en/{name}/">',
    ])
    page = (page.replace("__HEAD_SEO__", head).replace("__ASSETS__", "../assets/" if lang == "ru" else "../../assets/").replace("__LANG__", lang)
                .replace("__TITLE__", m["title"]).replace("__META_DESC__", m["desc"]).replace("__CANONICAL__", canonical)
                .replace("__OG_IMAGE__", BASE_URL + "/assets/og-" + lang + ".png")
                .replace("__RU_HREF__", "./" if lang == "ru" else f"../../{name}/").replace("__EN_HREF__", f"../en/{name}/" if lang == "ru" else "./")
                .replace("__RU_CUR__", 'aria-current="page"' if lang == "ru" else "").replace("__EN_CUR__", 'aria-current="page"' if lang == "en" else "")
                .replace("__ANALYTICS__", analytics_html()))
    page = page.replace(' >', '>')
    assert "__" not in page.replace("--", ""), "unfilled placeholder"
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out

for lang in ("ru", "en"):
    print("built", build(lang))
    for name in SUBPAGES:
        print("built", build_subpage(name, lang))

today = datetime.date.today().isoformat()
(ROOT / "robots.txt").write_text(f"""User-agent: *
Allow: /

# ИИ-краулеры разрешены явно: страница рассчитана на ответы в ChatGPT, Perplexity, Claude, Gemini, Нейро
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: YandexBot
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
""", encoding="utf-8")

SUB_URLS = "".join(
    f"""  <url><loc>{BASE_URL}{pre}/{name}/</loc><lastmod>{today}</lastmod>
    <xhtml:link rel="alternate" hreflang="ru" href="{BASE_URL}/{name}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/en/{name}/"/></url>
""" for name in SUBPAGES for pre in ("", "/en"))
(ROOT / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>{BASE_URL}/</loc><lastmod>{today}</lastmod>
    <xhtml:link rel="alternate" hreflang="ru" href="{BASE_URL}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/en/"/></url>
  <url><loc>{BASE_URL}/en/</loc><lastmod>{today}</lastmod>
    <xhtml:link rel="alternate" hreflang="ru" href="{BASE_URL}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE_URL}/en/"/></url>
{SUB_URLS}</urlset>
""", encoding="utf-8")

(ROOT / "llms.txt").write_text(f"""# OwnAgent

> Turnkey, hardened installation of a personal AI agent (Hermes Agent by Nous Research, or OpenClaw) on the client's own VPS. The agent and its data stay on the client's server. Fixed price, done within one working day, with a written report on 14 security and reliability checks.

## What is included (Personal, $99 one-time / 9 900 RUB; launch price for the first 20 installs, then $149 / 14 900 RUB)
- Hermes Agent or OpenClaw, client's choice, on the client's Ubuntu 22.04/24.04 VPS at any provider
- Telegram channel with the client's own bot token
- Model access via OpenRouter with a monthly spending cap
- Hardening: only SSH open from outside, agent panel on localhost, SSH keys only, root login disabled, fail2ban, unattended security updates, agent runs unprivileged under systemd
- Daily memory backup with a tested restore; downtime alert to Telegram
- Skills from an allowlist only, marketplace disabled
- Report on 14 checks with the external port scan and the agent's security audit attached, one-page guide, 14 days of support, 14-day refund, 30-day install guarantee
- Agent version pinned without known CVEs, snapshot before updates with tested rollback; nothing depends on the provider's account after handover

## Business (from $390 one-time / from 39 000 RUB)
Personal plus two integrations (Gmail, Google Calendar, Notion, Jira, Bitrix24, WhatsApp, Slack, Discord, n8n) with minimal permissions, an express security audit with a prioritized report, a setup call, 30 days of support. Optional support plan: $19/month (1 900 RUB).

## Why not one-click hosting
One-click hosts run the agent on their servers and often expose it to the internet. In February 2026 SecurityScorecard found 40,214 exposed OpenClaw instances (63% vulnerable), Snyk found 534 marketplace skills with critical findings and 76 confirmed malicious, and CVE-2026-25253 (one-click RCE) was followed by CVE-2026-33579 in March. OwnAgent installs on the client's server behind closed ports and holds no standing access after handover.

## Pages
- English: {BASE_URL}/en/
- Russian: {BASE_URL}/
- Sample report format (14 checks, placeholder values): {BASE_URL}/en/report/
- Privacy policy: {BASE_URL}/en/privacy/

## Contact
- Telegram: https://t.me/pasee2
- Email: aka.alius@gmail.com
""", encoding="utf-8")
print("robots.txt, sitemap.xml, llms.txt written")
