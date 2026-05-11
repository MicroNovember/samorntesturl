import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

CHANNELS = {
    "True Sport 7": "https://dookeela4.live/live-tv/tsp7",
    "Cartoon Network": "https://dookeela4.live/live-tv/cartoon-network",
    "True Sport HD 2": "https://dookeela4.live/live-tv/ts-hd2"
}

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    try:
        # ตรวจสอบว่ารันบน GitHub หรือไม่
        if os.environ.get("GITHUB_ACTIONS"):
            print("🤖 Running on GitHub Actions")
            options.binary_location = "/usr/bin/google-chrome"
            service = Service("/usr/bin/chromedriver")
        else:
            print("🏠 Running locally")
            service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ WebDriver initialized successfully")
        return driver
        
    except Exception as e:
        print(f"❌ Error initializing WebDriver: {e}")
        raise

def scan():
    print("🚀 Starting M3U8 Scanner...")
    playlist = {"groups": [{"name": "LIVE", "stations": []}]}
    
    try:
        driver = get_driver()
        print("🌐 WebDriver ready, starting scan...")
    except Exception as e:
        print(f"❌ Failed to initialize WebDriver: {e}")
        return
    
    for name, url in CHANNELS.items():
        try:
            print(f"\n🔍 Scanning: {name}")
            print(f"📍 URL: {url}")
            
            driver.get(url)
            print("⏳ Waiting 20 seconds for page to load...")
            time.sleep(20)
            
            # Debug: ดูว่า page title คืออะไร
            title = driver.title
            print(f"📄 Page title: {title}")
            
            # วิธีที่ 1: Performance logs
            logs = driver.get_log("performance")
            print(f"📊 Found {len(logs)} performance logs")
            
            found_m3u8 = False
            for entry in logs:
                msg = json.loads(entry["message"])["message"]
                if "params" in msg and "request" in msg["params"]:
                    target = msg["params"]["request"].get("url", "")
                    if ".m3u8" in target:
                        print(f"🎯 Found M3U8: {target}")
                        playlist["groups"][0]["stations"].append({"name": name, "url": target})
                        print(f"✅ Added {name} to playlist")
                        found_m3u8 = True
                        break
            
            # วิธีที่ 2: หาใน page source
            if not found_m3u8:
                print("🔍 Searching in page source...")
                page_source = driver.page_source
                import re
                m3u8_patterns = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', page_source)
                
                for pattern in m3u8_patterns:
                    if "index" in pattern or "master" in pattern or "playlist" in pattern:
                        print(f"🎯 Found M3U8 in source: {pattern}")
                        playlist["groups"][0]["stations"].append({"name": name, "url": pattern})
                        print(f"✅ Added {name} to playlist")
                        found_m3u8 = True
                        break
            
            # วิธีที่ 3: รอและค้นหาอีกครั้ง
            if not found_m3u8:
                print("⏳ Waiting 10 more seconds and retrying...")
                time.sleep(10)
                
                # หา video elements
                videos = driver.find_elements("tag name", "video")
                for video in videos:
                    src = video.get_attribute("src")
                    if src and ".m3u8" in src:
                        print(f"🎯 Found M3U8 in video element: {src}")
                        playlist["groups"][0]["stations"].append({"name": name, "url": src})
                        print(f"✅ Added {name} to playlist")
                        found_m3u8 = True
                        break
            
            if not found_m3u8:
                print(f"❌ No M3U8 found for {name}")
                
        except Exception as e:
            print(f"❌ Error scanning {name}: {e}")
    
    try:
        driver.quit()
        print("🔚 WebDriver closed")
    except:
        pass
    
    # แสดงสรุป
    total_found = len(playlist["groups"][0]["stations"])
    print(f"\n📋 Scan completed! Found {total_found} stations")
    
    # บันทึกผลลัพธ์
    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(playlist, f, ensure_ascii=False, indent=2)
    
    print("💾 Saved to playlist.json")
    
    if total_found == 0:
        print("⚠️ No M3U8 streams found. This could be due to:")
        print("   - Website blocking")
        print("   - Changed stream URLs")
        print("   - Network issues")

if __name__ == "__main__":
    scan()
