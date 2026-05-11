#!/usr/bin/env python3
"""
ตัวอย่างไฟล์ Python สำหรับ Web Scraping
เหมาะสำหรับรันบน GitHub Actions (ใช้ requests + BeautifulSoup)
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

def scrape_website(url):
    """ดึงข้อมูลจากเว็บไซต์"""
    print(f"🌐 Scraping: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # ดึงข้อมูลพื้นฐาน
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # ดึงลิงก์ทั้งหมด
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip()
            if text and href.startswith('http'):
                links.append({"text": text[:50], "url": href})
        
        # ดึงข้อมูลจาก meta tags
        meta_data = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            if name and content:
                meta_data[name] = content[:100]
        
        result = {
            "url": url,
            "title": title_text,
            "status_code": response.status_code,
            "scraped_at": datetime.now().isoformat(),
            "links_found": len(links),
            "sample_links": links[:5],  # เอาแค่ 5 ลิงก์แรก
            "meta_data": meta_data
        }
        
        print(f"✅ Scraped successfully - Found {len(links)} links")
        return result
        
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return {
            "url": url,
            "error": str(e),
            "scraped_at": datetime.now().isoformat()
        }

def main():
    """ฟังก์ชันหลัก"""
    print("=" * 60)
    print("🕷️  Web Scraper - GitHub Actions Edition")
    print("=" * 60)
    
    # เว็บไซต์ตัวอย่าง (public APIs/websites)
    websites = [
        "https://httpbin.org/html",
        "https://jsonplaceholder.typicode.com",
        "https://reqres.in"
    ]
    
    results = []
    
    for website in websites:
        result = scrape_website(website)
        results.append(result)
        time.sleep(1)  # รอ 1 วินาทีระหว่าง request
    
    # บันทึกผลลัพธ์
    output = {
        "scrape_session": {
            "started_at": datetime.now().isoformat(),
            "environment": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") else "Local",
            "total_websites": len(websites),
            "successful_scrapes": len([r for r in results if "error" not in r])
        },
        "results": results
    }
    
    with open("scraping_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # สร้างรายงานสรุป
    print("\n📊 Scraping Summary:")
    print(f"   Total websites: {len(websites)}")
    print(f"   Successful: {len([r for r in results if 'error' not in r])}")
    print(f"   Failed: {len([r for r in results if 'error' in r])}")
    
    print("\n🎉 Web scraping completed!")
    print("📄 Results saved to scraping_results.json")

if __name__ == "__main__":
    main()
