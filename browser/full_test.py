"""
Full Browser Test Script
- Google search karo
- YouTube browse karo  
- GitHub browse karo
- Wikipedia browse karo
- Har jagah scroll, click, screenshots lo
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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()

        # =============================================
        # TEST 1: Google
        # =============================================
        print("\n🌐 TEST 1: Google.com")
        await page.goto("https://www.google.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=ss_path("01_google_home"))
        print("✅ Google home loaded")

        # Search karo
        await page.fill("textarea[name='q']", "GitHub Codespaces AI browser automation")
        await page.screenshot(path=ss_path("02_google_typed"))
        await page.keyboard.press("Enter")
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=ss_path("03_google_results"))
        print("✅ Google search done")

        # Scroll down
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=ss_path("04_google_scrolled"))
        print("✅ Google scrolled")

        # =============================================
        # TEST 2: GitHub
        # =============================================
        print("\n🐙 TEST 2: GitHub.com")
        await page.goto("https://github.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=ss_path("05_github_home"))
        print("✅ GitHub home loaded")

        # Trending pe jao
        await page.goto("https://github.com/trending", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=ss_path("06_github_trending"))
        print("✅ GitHub trending loaded")

        # Scroll
        await page.mouse.wheel(0, 600)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=ss_path("07_github_trending_scrolled"))

        # =============================================
        # TEST 3: Wikipedia
        # =============================================
        print("\n📚 TEST 3: Wikipedia")
        await page.goto("https://en.wikipedia.org/wiki/Artificial_intelligence", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=ss_path("08_wikipedia_ai"))
        print("✅ Wikipedia AI page loaded")

        # Table of contents click
        try:
            await page.click("text=Machine learning", timeout=3000)
            await page.wait_for_timeout(1500)
            await page.screenshot(path=ss_path("09_wikipedia_ml_section"))
            print("✅ Wikipedia section clicked")
        except:
            await page.mouse.wheel(0, 800)
            await page.screenshot(path=ss_path("09_wikipedia_scrolled"))

        # =============================================
        # TEST 4: YouTube
        # =============================================
        print("\n▶️  TEST 4: YouTube")
        await page.goto("https://www.youtube.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=ss_path("10_youtube_home"))
        print("✅ YouTube home loaded")

        # Search karo
        try:
            await page.click("input#search", timeout=5000)
            await page.type("input#search", "Python programming tutorial", delay=50)
            await page.screenshot(path=ss_path("11_youtube_search_typed"))
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=ss_path("12_youtube_results"))
            print("✅ YouTube search done")
        except Exception as e:
            print(f"⚠️ YouTube search: {e}")
            await page.screenshot(path=ss_path("11_youtube_fallback"))

        # =============================================
        # TEST 5: Reddit
        # =============================================
        print("\n🔴 TEST 5: Reddit")
        await page.goto("https://www.reddit.com/r/programming/", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=ss_path("13_reddit_programming"))
        print("✅ Reddit r/programming loaded")

        await page.mouse.wheel(0, 700)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=ss_path("14_reddit_scrolled"))

        # =============================================
        # TEST 6: Speed Test (fast.com)
        # =============================================
        print("\n⚡ TEST 6: Fast.com (Speed check)")
        await page.goto("https://fast.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        await page.screenshot(path=ss_path("15_fast_com"))
        print("✅ Fast.com loaded")

        # =============================================
        # SUMMARY
        # =============================================
        print("\n" + "="*50)
        print("✅ SARE TESTS COMPLETE!")
        print(f"📸 Screenshots saved in: {SS_DIR}/")
        print("="*50)

        ss_files = sorted(os.listdir(SS_DIR))
        print(f"\n📋 Total screenshots: {len(ss_files)}")
        for f in ss_files:
            print(f"  - {f}")

        await browser.close()

asyncio.run(test_browser())
