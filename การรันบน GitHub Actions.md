การรันบน GitHub Actions เป็นวิธีที่ฉลาดมากครับ เพราะฟรีและทำงานเบื้องหลังได้ตลอดเวลา แต่หัวใจสำคัญคือ "สภาพแวดล้อมของ GitHub Actions คือ Linux (Ubuntu)" ดังนั้นเราต้องปรับโค้ด .py เล็กน้อยเพื่อให้มันหา Chrome ในระบบเจอ

นี่คือแผนการรันให้สำเร็จครับ

1. เตรียมโค้ด Python (scanner.py)
เซฟโค้ดนี้ไว้ในโปรเจกต์ของคุณ โค้ดนี้ถูกปรับให้ทำงานได้ทั้งบน Windows (เครื่องคุณ) และ Linux (GitHub) โดยอัตโนมัติครับ

Python
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
2. สร้างไฟล์ Workflow (.github/workflows/main.yml)
สร้างโฟลเดอร์ชื่อ .github และโฟลเดอร์ย่อย workflows จากนั้นสร้างไฟล์ชื่อ main.yml แล้วใส่โค้ดนี้ลงไปครับ

YAML
name: Auto Scan M3U8
on:
  schedule:
    - cron: '0 */4 * * *' # รันทุก 4 ชั่วโมง
  workflow_dispatch:      # กดปุ่มรันเองได้ในหน้า Actions

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Chrome and Driver
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable chromium-chromedriver

      - name: Install Dependencies
        run: |
          pip install selenium webdriver-manager

      - name: Run Scanner
        run: python scanner.py

      - name: Commit and Push
        run: |
          git config --global user.name 'GitHub Action'
          git config --global user.email 'action@github.com'
          git add playlist.json
          git commit -m "Update playlist.json [Skip CI]" || exit 0
          git push
3. สิ่งที่ต้องทำเพื่อให้มันทำงาน
Push ขึ้น GitHub: นำไฟล์ทั้งหมดขึ้น Repo ของคุณ

ตั้งค่า Permission:

ไปที่หน้า GitHub Repo ของคุณ

คลิก Settings > Actions > General

เลื่อนลงไปที่ Workflow permissions

เลือก "Read and write permissions" (สำคัญมาก! เพื่อให้ Bot สามารถเซฟไฟล์ playlist.json กลับเข้า Repo ได้)

กด Save

ทดสอบรัน:

ไปที่แถบ Actions ด้านบนของ GitHub

เลือกเมนู Auto Scan M3U8 ทางซ้าย

กดปุ่ม Run workflow ด้านขวา