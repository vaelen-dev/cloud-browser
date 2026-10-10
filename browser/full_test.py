"""
Full Browser Test Script - v2 (Fixed selectors + robust error handling)
Tests: Google, GitHub, Wikipedia, YouTube, Reddit, Fast.com
"""
import asyncio
import os
from playwright.async_api import async_playwright
from datetime import datetime

SS_DIR = "screenshots"
os.makedirs(SS_DIR, exist_ok=True)

def ss_path(name):
    t = datetime.now().strftime("%H%M%S")
    return f"{SS_DIR}/{t}_{name}.png"

async def safe_fill(page, selectors, text, timeout=5000):
    """Multiple selectors try karo"""
    for sel in selectors:
        try:
            await page.wait_for_selector(sel, timeout=timeout)
            await page.fill(sel, text)
            return True
        except:
            continue
    return False

async def safe_click(page, selectors, timeout=4000):
    """Multiple selectors try karo click ke liye"""
    for sel in selectors:
        try:
            await page.click(sel, timeout=timeout)
            return True
        except:
            continue
    return False

async def test_browser():
    async with async_playwright() as p:
        print("🚀 Browser launch ho raha hai...")
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--window-size=1280,720"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # =============================================
        # TEST 1: Google
        # =============================================
        print("\n🌐 TEST 1: Google.com")
        try:
            await page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=ss_path("01_google_home"))
            print("✅ Google home loaded")

            filled = await safe_fill(page, [
                "textarea[name='q']",
                "input[name='q']",
                "[aria-label='Search']",
                "input[type='text']"
            ], "GitHub Codespaces AI browser automation")

            if filled:
                await page.screenshot(path=ss_path("02_google_typed"))
                await page.keyboard.press("Enter")
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(2000)
                await page.screenshot(path=ss_path("03_google_results"))
                await page.mouse.wheel(0, 500)
                await page.wait_for_timeout(1000)
                await page.screenshot(path=ss_path("04_google_scrolled"))
                print("✅ Google search + scroll done")
            else:
                print("⚠️ Google search box nahi mila — skip")
        except Exception as e:
            print(f"⚠️ Google test error: {e}")
            await page.screenshot(path=ss_path("01_google_error"))

        # =============================================
        # TEST 2: GitHub
        # =============================================
        print("\n🐙 TEST 2: GitHub.com")
        try:
            await page.goto("https://github.com", wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=ss_path("05_github_home"))
            print("✅ GitHub home loaded")

            await page.goto("https://github.com/trending", wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=ss_path("06_github_trending"))
            await page.mouse.wheel(0, 600)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=ss_path("07_github_trending_scrolled"))
            print("✅ GitHub trending + scroll done")
        except Exception as e:
            print(f"⚠️ GitHub test error: {e}")
            await page.screenshot(path=ss_path("05_github_error"))

        # =============================================
        # TEST 3: Wikipedia
        # =============================================
        print("\n📚 TEST 3: Wikipedia")
        try:
            await page.goto("https://en.wikipedia.org/wiki/Artificial_intelligence", wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=ss_path("08_wikipedia_ai"))
            print("✅ Wikipedia AI page loaded")

            await page.mouse.wheel(0, 600)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=ss_path("09_wikipedia_scrolled"))
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=ss_path("10_wikipedia_deep_scroll"))
            print("✅ Wikipedia scroll done")
        except Exception as e:
            print(f"⚠️ Wikipedia test error: {e}")
            await page.screenshot(path=ss_path("08_wikipedia_error"))

        # =============================================
        # TEST 4: YouTube
        # =============================================
        print("\n▶️  TEST 4: YouTube")
        try:
            await page.goto("https://www.youtube.com", wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=ss_path("11_youtube_home"))
            print("✅ YouTube home loaded")

            filled = await safe_fill(page, [
                "input#search",
                "input[name='search_query']",
                "[placeholder='Search']"
            ], "Python programming tutorial")

            if filled:
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)
                await page.screenshot(path=ss_path("12_youtube_results"))
                await page.mouse.wheel(0, 500)
                await page.wait_for_timeout(1000)
                await page.screenshot(path=ss_path("13_youtube_scrolled"))
                print("✅ YouTube search done")
            else:
                print("⚠️ YouTube search box nahi mila")
        except Exception as e:
            print(f"⚠️ YouTube test error: {e}")
            await page.screenshot(path=ss_path("11_youtube_error"))

        # =============================================
        # TEST 5: Reddit
        # =============================================
        print("\n🔴 TEST 5: Reddit")
        try:
            await page.goto("https://www.reddit.com/r/programming/", wait_until="domcontentloaded", timeout=25000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=ss_path("14_reddit_programming"))
            await page.mouse.wheel(0, 700)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=ss_path("15_reddit_scrolled"))
            await page.mouse.wheel(0, 700)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=ss_path("16_reddit_deep"))
            print("✅ Reddit browse done")
        except Exception as e:
            print(f"⚠️ Reddit test error: {e}")
            await page.screenshot(path=ss_path("14_reddit_error"))

        # =============================================
        # TEST 6: Fast.com
        # =============================================
        print("\n⚡ TEST 6: Fast.com")
        try:
            await page.goto("https://fast.com", wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(5000)
            await page.screenshot(path=ss_path("17_fast_com"))
            print("✅ Fast.com loaded")
        except Exception as e:
            print(f"⚠️ Fast.com error: {e}")

        # =============================================
        # SUMMARY
        # =============================================
        ss_files = sorted(os.listdir(SS_DIR))
        print(f"\n{'='*50}")
        print(f"✅ TESTS COMPLETE! Total screenshots: {len(ss_files)}")
        print(f"{'='*50}")
        for f in ss_files:
            size = os.path.getsize(f"{SS_DIR}/{f}") // 1024
            print(f"  📸 {f} ({size} KB)")

        await browser.close()

asyncio.run(test_browser())
