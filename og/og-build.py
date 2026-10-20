#!/usr/bin/env python3
"""Рендерит OG-картинки 1200x630 из HTML через headless Chrome. Запуск: python3 og/og-build.py"""
import pathlib, subprocess, html
ROOT = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KEY = (ROOT / "fonts/key.svg").read_text().replace('fill="currentColor"', 'fill="#e8a33d"')
CHAT = (ROOT / "fonts/chat.svg").read_text().replace('fill="currentColor"', 'fill="#e8a33d"')
SHIELD = (ROOT / "fonts/shield.svg").read_text().replace('fill="currentColor"', 'fill="#e8a33d"')
MARK = '<svg viewBox="0 0 64 64" width="44" height="44"><rect x="4" y="4" width="56" height="56" rx="12" fill="#15181b"/><rect x="18" y="18" width="28" height="28" rx="6" fill="none" stroke="#e8a33d" stroke-width="5"/><rect x="28" y="28" width="8" height="8" rx="2" fill="#e8a33d"/></svg>'

CSS = """
@font-face{font-family:G;src:url(fonts/GolosText[wght].ttf);font-weight:100 900}
@font-face{font-family:M;src:url(fonts/JetBrainsMono[wght].ttf);font-weight:100 900}
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden;background:#0f1113;color:#e9ebe6;font-family:G,sans-serif;-webkit-font-smoothing:antialiased}
.page{position:relative;width:1200px;height:630px;padding:56px 64px}
.brand{position:absolute;left:64px;top:52px;display:flex;align-items:center;gap:14px;font-weight:700;font-size:28px;letter-spacing:-.01em}
.url{position:absolute;right:64px;bottom:50px;font-family:M;font-size:20px;color:#8f968f}
.foot{position:absolute;left:64px;bottom:50px;font-family:M;font-size:20px;color:#8f968f}
.foot b{color:#e8a33d;font-weight:500}
h1{font-weight:800;letter-spacing:-.035em;line-height:1.02}
.acc{color:#e8a33d}
.mut{color:#5f666a}
"""

def chrome(html_path, out):
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1200,630", f"--screenshot={out}", f"file://{html_path}"],
                   check=True, capture_output=True)

T = {
 "en": dict(a1="Your AI agent.", a2="Your server.", a3="Your keys.",
            afoot="Hermes · OpenClaw · hardened install · <b>$99</b>",
            b1="14 security checks.", b2a="One day.", b2b="Your VPS.", bfoot="Hermes or OpenClaw, installed and locked down · <b>$99</b>",
            c1="40,214 OpenClaw instances", c2="exposed to the internet.", c3="Yours won't be.",
            cfoot="Hardened install on your own VPS · <b>$99</b>",
            d1="Your AI agent in Telegram.", d2="On your own server.", d3="Ready tomorrow.", dsize=66,
            dfoot="No terminal needed · locked down by default · <b>$99</b>",
            term=["# client server, SSH tunnel only", "$ ownagent install --agent hermes --channel telegram",
                  "✓ only 22/tcp open outside, gateway on 127.0.0.1", "✓ fail2ban, unattended security updates",
                  "✓ agent unprivileged, version pinned, no known CVEs", "✓ OpenRouter connected, cap $30/mo",
                  "✓ Telegram: @your_agent_bot replies", "✓ daily memory backup, restore tested",
                  "✓ snapshot before updates, rollback tested", "✓ temporary access key removed",
                  "# 14 checks passed, report sent to owner"]),
 "ru": dict(a1="Ваш ИИ-агент.", a2="Ваш сервер.", a3="Ваши ключи.",
            afoot="Hermes · OpenClaw · установка с защитой · <b>9 900 ₽</b>",
            b1="14 проверок безопасности.", b2a="Один день.", b2b="Ваш VPS.", bfoot="Hermes или OpenClaw, установлен и закрыт · <b>9 900 ₽</b>",
            c1="40 214 инстансов OpenClaw", c2="открыты в интернет.", c3="Ваш не будет.",
            cfoot="Защищённая установка на вашем VPS · <b>9 900 ₽</b>",
            d1="Личный ИИ-агент в Telegram.", d2="На вашем сервере.", d3="Готов завтра.", dsize=58,
            dfoot="Без терминала · закрыт от чужих по умолчанию · <b>9 900 ₽</b>",
            term=["# сервер клиента, доступ только по SSH-туннелю", "$ ownagent install --agent hermes --channel telegram",
                  "✓ снаружи открыт только 22/tcp, gateway на 127.0.0.1", "✓ fail2ban, обновления безопасности",
                  "✓ агент не от root, версия закреплена, без CVE", "✓ OpenRouter подключён, лимит 3 000 ₽/мес",
                  "✓ Telegram: @your_agent_bot отвечает", "✓ бэкап памяти ежедневно, восстановление проверено",
                  "✓ снапшот перед обновлением, откат проверен", "✓ временный ключ доступа удалён",
                  "# 14 проверок пройдено, отчёт отправлен владельцу"]),
}

def variant_a(t):
    return f"""<div class="page">
<div class="brand">{MARK} OwnAgent</div>
<div style="position:absolute;left:64px;top:170px;width:760px">
  <h1 style="font-size:92px">{t['a1']}<br>{t['a2']}<br><span class="acc">{t['a3']}</span></h1>
</div>
<div style="position:absolute;right:72px;top:150px;width:300px;height:300px;display:grid;place-items:center;border-radius:28px;background:#15181b;border:1px solid rgba(255,255,255,.1)">
  <div style="width:190px;height:190px">{KEY}</div>
</div>
<div class="foot">{t['afoot']}</div><div class="url">getownagent.com</div></div>"""

def variant_b(t):
    rows = "".join(f'<div class="{ "c" if l.startswith("#") else "ok" if l.startswith("✓") else "p"}">{html.escape(l)}</div>' for l in t["term"])
    return f"""<style>
.term{{position:absolute;right:52px;top:118px;width:600px;background:#15181b;border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:22px 26px;font-family:M;font-size:16px;line-height:1.7;white-space:nowrap;overflow:hidden;color:#c3c7c0;transform:rotate(-2deg);box-shadow:0 40px 120px -40px rgba(0,0,0,.8)}}
.term .c{{color:#8f968f}} .term .ok{{color:#7cc77a}} .term .p{{color:#e9ebe6}}
.term .ok::first-letter{{color:#7cc77a}}
</style><div class="page">
<div class="brand">{MARK} OwnAgent</div>
<div class="term">{rows}</div>
<div style="position:absolute;left:64px;top:190px;width:500px">
  <h1 style="font-size:60px">{t['b1']}<br><span class="acc">{t['b2a']}<br>{t['b2b']}</span></h1>
</div>
<div class="foot">{t['bfoot']}</div><div class="url">getownagent.com</div></div>"""

def variant_c(t):
    return f"""<div class="page">
<div class="brand">{MARK} OwnAgent</div>
<div style="position:absolute;left:64px;top:150px;width:1080px">
  <h1 class="mut" style="font-size:64px;font-weight:700">{t['c1']}<br>{t['c2']}</h1>
  <h1 class="acc" style="font-size:112px;margin-top:34px">{t['c3']}</h1>
</div>
<div style="position:absolute;right:64px;top:56px;width:64px;height:64px">{SHIELD}</div>
<div class="foot">{t['cfoot']}</div><div class="url">getownagent.com</div></div>"""

def variant_d(t):
    return f"""<div class="page">
<div class="brand">{MARK} OwnAgent</div>
<div style="position:absolute;left:64px;top:170px;width:860px">
  <h1 style="font-size:{t['dsize']}px">{t['d1']}<br>{t['d2']}<br><span class="acc">{t['d3']}</span></h1>
</div>
<div style="position:absolute;right:72px;top:170px;width:260px;height:260px;display:grid;place-items:center;border-radius:28px;background:#15181b;border:1px solid rgba(255,255,255,.1)">
  <div style="width:160px;height:160px">{CHAT}</div>
</div>
<div class="foot">{t['dfoot']}</div><div class="url">getownagent.com</div></div>"""

out = ROOT / "out"; out.mkdir(exist_ok=True)
for lang, t in T.items():
    for name, fn in (("a-key", variant_a), ("b-terminal", variant_b), ("c-contrast", variant_c), ("d-outcome", variant_d)):
        p = ROOT / f"_{name}-{lang}.html"
        p.write_text(f'<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>{CSS}</style>{fn(t)}</html>', encoding="utf-8")
        png = out / f"og-{name}-{lang}.png"
        chrome(p, png); p.unlink()
        print("rendered", png.name)
