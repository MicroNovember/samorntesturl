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
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # ตรวจสอบว่ารันบน GitHub หรือไม่ ถ้าใช่ให้ใช้ Path ที่ GitHub เตรียมไว้
    if os.environ.get("GITHUB_ACTIONS"):
        options.binary_location = "/usr/bin/google-chrome"
        service = Service("/usr/bin/chromedriver")
    else:
        # สำหรับรันบน Windows เครื่องตัวเอง
        service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scan():
    playlist = {"groups": [{"name": "LIVE", "stations": []}]}
    driver = get_driver()
    
    for name, url in CHANNELS.items():
        try:
            print(f"Scanning: {name}")
            driver.get(url)
            time.sleep(15) # รอให้ไฟล์ m3u8 โผล่
            
            logs = driver.get_log("performance")
            for entry in logs:
                msg = json.loads(entry["message"])["message"]
                if "params" in msg and "request" in msg["params"]:
                    target = msg["params"]["request"].get("url", "")
                    if ".m3u8" in target and ("index" in target or "master" in target):
                        playlist["groups"][0]["stations"].append({"name": name, "url": target})
                        print(f"✅ Found: {name}")
                        break
        except Exception as e:
            print(f"❌ Error {name}: {e}")
            
    driver.quit()
    
    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(playlist, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scan()
