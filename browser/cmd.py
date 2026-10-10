"""
CLI Command Runner for Instant Cloud Browser Control
Usage:
  python cmd.py goto https://example.com
  python cmd.py click "button_text"
  python cmd.py type "#selector" "text_to_type"
  python cmd.py key "Enter"
  python cmd.py scroll down 500
  python cmd.py info
"""

import sys
import json
import asyncio
import os
from playwright.async_api import async_playwright

BROWSER_DATA = "/workspaces/cloud-browser/browser-data"
SS_DIR = "/workspaces/cloud-browser/screenshots"
os.makedirs(BROWSER_DATA, exist_ok=True)
os.makedirs(SS_DIR, exist_ok=True)

LATEST_SS = os.path.join(SS_DIR, "latest.png")

async def run():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No action specified"}))
        return

    action = sys.argv[1].lower()
    args = sys.argv[2:]

    async with async_playwright() as pw:
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=BROWSER_DATA,
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--window-size=1280,900"],
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else await context.new_page()

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
                await page.wait_for_timeout(1500)

            elif action == "type":
                selector = args[0]
                text = args[1] if len(args) > 1 else ""
                await page.fill(selector, "")
                await page.type(selector, text, delay=30)
                await page.wait_for_timeout(500)

            elif action == "key":
                key = args[0]
                await page.keyboard.press(key)
                await page.wait_for_timeout(1500)

            elif action == "scroll":
                direction = args[0] if args else "down"
                amt = int(args[1]) if len(args) > 1 else 500
                dy = amt if direction == "down" else -amt
                await page.mouse.wheel(0, dy)
                await page.wait_for_timeout(1000)

            elif action == "info":
                links = await page.eval_on_selector_all("a", "els => els.map(e => ({text: e.innerText.trim().slice(0,40), href: e.href})).filter(x => x.text)")
                buttons = await page.eval_on_selector_all("button", "els => els.map(e => e.innerText.trim().slice(0,40)).filter(x => x)")
                inputs = await page.eval_on_selector_all("input", "els => els.map(e => ({type: e.type, placeholder: e.placeholder, name: e.name}))")
                res["links"] = links[:12]
                res["buttons"] = buttons[:10]
                res["inputs"] = inputs[:10]

            # Take latest screenshot
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

        finally:
            await context.close()

        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    asyncio.run(run())
