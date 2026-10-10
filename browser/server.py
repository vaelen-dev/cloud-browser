"""
Browser Control Server
======================
Ek baar start karo — main directly HTTP requests bhejta rahunga.
Port 8080 pe chalta hai. Codespace mein port public kar do.
"""

import asyncio
import base64
import os
import traceback
from contextlib import asynccontextmanager
from io import BytesIO

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# ── State ──────────────────────────────────────────────────────────────
BROWSER_DATA = "/workspaces/cloud-browser/browser-data"
os.makedirs(BROWSER_DATA, exist_ok=True)

state: dict = {}   # holds playwright, context, page

# ── Lifespan: browser start/stop ───────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Browser start ho raha hai...")
    pw = await async_playwright().start()
    context = await pw.chromium.launch_persistent_context(
        user_data_dir=BROWSER_DATA,
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--window-size=1280,900"],
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )
    page = context.pages[0] if context.pages else await context.new_page()
    state.update(pw=pw, context=context, page=page)
    print("✅ Browser ready! Server chal raha hai port 8080 pe.")
    yield
    await context.close()
    await pw.stop()
    print("Browser band ho gaya.")

app = FastAPI(title="Cloud Browser API", lifespan=lifespan)

# ── Helper ─────────────────────────────────────────────────────────────
async def get_screenshot() -> str:
    """Screenshot lo aur base64 string return karo"""
    page: Page = state["page"]
    buf = await page.screenshot(type="png")
    return base64.b64encode(buf).decode()

def ok(data: dict = None, **kwargs):
    return JSONResponse({"status": "ok", **(data or {}), **kwargs})

def err(msg: str):
    return JSONResponse({"status": "error", "message": msg}, status_code=500)

# ── Routes ─────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    page: Page = state["page"]
    return ok(url=page.url, title=await page.title())


@app.get("/screenshot")
async def screenshot():
    """Abhi ka screenshot lo"""
    try:
        img = await get_screenshot()
        page: Page = state["page"]
        return ok(image=img, url=page.url, title=await page.title())
    except Exception as e:
        return err(str(e))


@app.post("/goto")
async def goto(url: str, wait: int = 2000):
    """Kisi URL pe jao"""
    try:
        page: Page = state["page"]
        if not url.startswith("http"):
            url = "https://" + url
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(wait)
        img = await get_screenshot()
        return ok(image=img, url=page.url, title=await page.title())
    except Exception as e:
        return err(traceback.format_exc())


@app.post("/click")
async def click(selector: str = None, text: str = None, x: float = None, y: float = None):
    """Kisi element pe click karo"""
    try:
        page: Page = state["page"]
        if text:
            await page.get_by_text(text).first.click(timeout=8000)
        elif selector:
            await page.click(selector, timeout=8000)
        elif x is not None and y is not None:
            await page.mouse.click(x, y)
        await page.wait_for_timeout(1500)
        img = await get_screenshot()
        return ok(image=img, url=page.url)
    except Exception as e:
        return err(traceback.format_exc())


@app.post("/type")
async def type_text(selector: str, text: str, clear: bool = True, delay: int = 40):
    """Kisi field mein text type karo"""
    try:
        page: Page = state["page"]
        if clear:
            await page.fill(selector, "")
        await page.type(selector, text, delay=delay)
        await page.wait_for_timeout(500)
        img = await get_screenshot()
        return ok(image=img)
    except Exception as e:
        return err(traceback.format_exc())


@app.post("/key")
async def press_key(key: str):
    """Keyboard key press karo (Enter, Tab, Escape, etc.)"""
    try:
        page: Page = state["page"]
        await page.keyboard.press(key)
        await page.wait_for_timeout(1500)
        img = await get_screenshot()
        return ok(image=img, url=page.url)
    except Exception as e:
        return err(traceback.format_exc())


@app.post("/scroll")
async def scroll(direction: str = "down", amount: int = 500):
    """Page scroll karo"""
    try:
        page: Page = state["page"]
        dy = amount if direction == "down" else -amount
        await page.mouse.wheel(0, dy)
        await page.wait_for_timeout(800)
        img = await get_screenshot()
        return ok(image=img)
    except Exception as e:
        return err(traceback.format_exc())


@app.post("/eval")
async def evaluate(script: str):
    """JavaScript run karo page pe"""
    try:
        page: Page = state["page"]
        result = await page.evaluate(script)
        img = await get_screenshot()
        return ok(result=str(result), image=img)
    except Exception as e:
        return err(traceback.format_exc())


@app.get("/info")
async def page_info():
    """Current page ki detailed info"""
    try:
        page: Page = state["page"]
        links = await page.eval_on_selector_all("a", "els => els.map(e => ({text: e.innerText.trim().slice(0,40), href: e.href}))")
        buttons = await page.eval_on_selector_all("button", "els => els.map(e => e.innerText.trim().slice(0,40))")
        inputs = await page.eval_on_selector_all("input", "els => els.map(e => ({type: e.type, placeholder: e.placeholder, name: e.name}))")
        img = await get_screenshot()
        return ok(
            url=page.url,
            title=await page.title(),
            links=links[:15],
            buttons=buttons[:10],
            inputs=inputs[:10],
            image=img
        )
    except Exception as e:
        return err(traceback.format_exc())


@app.post("/back")
async def go_back():
    page: Page = state["page"]
    await page.go_back()
    await page.wait_for_timeout(1500)
    return ok(image=await get_screenshot(), url=page.url)


@app.post("/forward")
async def go_forward():
    page: Page = state["page"]
    await page.go_forward()
    await page.wait_for_timeout(1500)
    return ok(image=await get_screenshot(), url=page.url)


@app.post("/reload")
async def reload():
    page: Page = state["page"]
    await page.reload(wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)
    return ok(image=await get_screenshot(), url=page.url)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
