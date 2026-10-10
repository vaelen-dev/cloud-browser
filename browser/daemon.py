"""
Continuous Cloud Browser Daemon
Keeps the browser and all open tabs alive in memory.
Listens on localhost:9000 for instant commands.
"""

import asyncio
import json
import os
import traceback
from playwright.async_api import async_playwright

BROWSER_DATA = "/workspaces/cloud-browser/browser-data"
SS_DIR = "/workspaces/cloud-browser/screenshots"
os.makedirs(BROWSER_DATA, exist_ok=True)
os.makedirs(SS_DIR, exist_ok=True)
LATEST_SS = os.path.join(SS_DIR, "latest.png")

state = {}

async def handle_client(reader, writer):
    data = await reader.read(4096)
    if not data:
        writer.close()
        return

    req = json.loads(data.decode())
    action = req.get("action", "").lower()
    args = req.get("args", [])
    page = state.get("page")

    res = {"action": action, "status": "ok"}

    try:
        if action == "goto":
            url = args[0] if args else "https://google.com"
            if not url.startswith("http"):
                url = "https://" + url
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)

        elif action == "click":
            target = args[0]
            try:
                await page.get_by_text(target).first.click(timeout=5000)
            except Exception:
                await page.click(target, timeout=5000)
            await page.wait_for_timeout(1000)

        elif action == "type":
            selector = args[0]
            text = args[1] if len(args) > 1 else ""
            await page.fill(selector, "")
            await page.type(selector, text, delay=30)
            await page.wait_for_timeout(500)

        elif action == "key":
            await page.keyboard.press(args[0])
            await page.wait_for_timeout(1000)

        elif action == "scroll":
            direction = args[0] if args else "down"
            amt = int(args[1]) if len(args) > 1 else 500
            dy = amt if direction == "down" else -amt
            await page.mouse.wheel(0, dy)
            await page.wait_for_timeout(800)

        elif action == "eval":
            script = args[0]
            val = await page.evaluate(script)
            res["result"] = str(val)

        elif action == "info":
            links = await page.eval_on_selector_all("a", "els => els.map(e => ({text: e.innerText.trim().slice(0,40), href: e.href})).filter(x => x.text)")
            buttons = await page.eval_on_selector_all("button", "els => els.map(e => e.innerText.trim().slice(0,40)).filter(x => x)")
            inputs = await page.eval_on_selector_all("input", "els => els.map(e => ({type: e.type, placeholder: e.placeholder, name: e.name}))")
            res["links"] = links[:12]
            res["buttons"] = buttons[:10]
            res["inputs"] = inputs[:10]

        # Always update screenshot
        await page.screenshot(path=LATEST_SS)
        res["url"] = page.url
        res["title"] = await page.title()
        res["screenshot"] = LATEST_SS

    except Exception as e:
        res["status"] = "error"
        res["message"] = str(e)
        try:
            await page.screenshot(path=LATEST_SS)
        except Exception:
            pass

    out_bytes = json.dumps(res).encode()
    writer.write(out_bytes)
    await writer.drain()
    writer.close()

async def main():
    async with async_playwright() as pw:
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=BROWSER_DATA,
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--window-size=1280,900"],
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        state["pw"] = pw
        state["context"] = context
        state["page"] = page

        server = await asyncio.start_server(handle_client, "127.0.0.1", 9000)
        print("Daemon running on 127.0.0.1:9000")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
