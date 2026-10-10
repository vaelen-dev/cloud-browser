"""
Cloud Browser Controller
========================
Yeh script Antigravity (AI) ko browser control karne deta hai.
Browser data /workspaces/cloud-browser/browser-data/ mein save hota hai.
Logins/cookies persist hote hain sessions ke beech.
"""

import asyncio
import os
import base64
from datetime import datetime
from playwright.async_api import async_playwright

# Persistent browser data path (logins yahan save honge)
BROWSER_DATA_DIR = "/workspaces/cloud-browser/browser-data"
SCREENSHOTS_DIR = "/workspaces/cloud-browser/screenshots"

os.makedirs(BROWSER_DATA_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


class CloudBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self, headless=False):
        """Browser start karo — data persist hoga"""
        print("🚀 Browser start ho raha hai...")
        self.playwright = await async_playwright().start()

        # Persistent context — logins/cookies save rehte hain
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=BROWSER_DATA_DIR,
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--remote-debugging-port=9222",
                "--window-size=1280,720",
            ],
            viewport={"width": 1280, "height": 720},
            locale="en-US",
        )

        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        print(f"✅ Browser ready! Current URL: {self.page.url}")
        return self

    async def goto(self, url):
        """Kisi URL pe jao"""
        print(f"🌐 Ja raha hoon: {url}")
        await self.page.goto(url, wait_until="domcontentloaded")
        await self.screenshot(f"goto_{url.replace('://', '_').replace('/', '_')[:30]}")
        print(f"✅ Page load ho gaya: {self.page.title()}")

    async def click(self, selector=None, text=None, x=None, y=None):
        """Kisi element pe click karo"""
        if text:
            print(f"🖱️  Click: '{text}' text wale element pe")
            await self.page.get_by_text(text).first.click()
        elif selector:
            print(f"🖱️  Click: {selector}")
            await self.page.click(selector)
        elif x and y:
            print(f"🖱️  Click: coordinates ({x}, {y})")
            await self.page.mouse.click(x, y)
        await self.screenshot("after_click")

    async def type_text(self, selector, text, clear_first=True):
        """Kisi field mein text type karo"""
        print(f"⌨️  Type karo: '{text[:20]}...' in {selector}")
        if clear_first:
            await self.page.fill(selector, "")
        await self.page.type(selector, text, delay=50)

    async def screenshot(self, name="screenshot"):
        """Screenshot lo aur save karo"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{SCREENSHOTS_DIR}/{timestamp}_{name}.png"
        await self.page.screenshot(path=filename, full_page=False)
        print(f"📸 Screenshot: {filename}")
        return filename

    async def get_text(self, selector):
        """Page se text nikalo"""
        element = await self.page.query_selector(selector)
        if element:
            return await element.inner_text()
        return None

    async def wait_for(self, selector, timeout=10000):
        """Kisi element ka wait karo"""
        print(f"⏳ Wait kar raha hoon: {selector}")
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def scroll(self, direction="down", amount=500):
        """Page scroll karo"""
        if direction == "down":
            await self.page.mouse.wheel(0, amount)
        else:
            await self.page.mouse.wheel(0, -amount)

    async def current_info(self):
        """Current page ki info"""
        info = {
            "url": self.page.url,
            "title": await self.page.title(),
        }
        print(f"📍 URL: {info['url']}")
        print(f"📄 Title: {info['title']}")
        return info

    async def close(self):
        """Browser band karo (data save rehega)"""
        print("💾 Data save ho raha hai aur browser band ho raha hai...")
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("✅ Done! Agla session mein login persist rahega.")


# ============================================================
# EXAMPLE USAGE — Yahan apna kaam likhein
# ============================================================
async def main():
    browser = CloudBrowser()
    await browser.start(headless=False)

    try:
        # Example: Google pe jao
        await browser.goto("https://www.google.com")
        await browser.current_info()

        # Yahan aur commands add karo...
        # await browser.goto("https://github.com")
        # await browser.click(text="Sign in")
        # await browser.type_text("#login_field", "your_username")

        # Screenshot dekho
        await browser.screenshot("final")

        print("\n✅ Kaam ho gaya! Screenshots dekho:", SCREENSHOTS_DIR)
        print("💡 Browser data save hai — agli baar login rahega!")

    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
