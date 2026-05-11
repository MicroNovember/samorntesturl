#!/usr/bin/env python3
"""
ตัวอย่างไฟล์ Python สำหรับรันบน GitHub Actions
"""

import datetime
import json
import os
import sys

def main():
    print("=" * 50)
    print("🐍 Python Script Running on GitHub Actions")
    print("=" * 50)
    
    # แสดงข้อมูลระบบ
    print(f"📅 Current time: {datetime.datetime.now()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Platform: {sys.platform}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # ตรวจสอบ environment variables ของ GitHub Actions
    if os.environ.get("GITHUB_ACTIONS"):
        print("✅ Running on GitHub Actions")
        print(f"🏢 Repository: {os.environ.get('GITHUB_REPOSITORY', 'Unknown')}")
        print(f"🌟 Workflow: {os.environ.get('GITHUB_WORKFLOW', 'Unknown')}")
    else:
        print("🏠 Running locally")
    
    # สร้างผลลัพธ์
    result = {
        "timestamp": datetime.datetime.now().isoformat(),
        "python_version": sys.version,
        "platform": sys.platform,
        "success": True,
        "message": "Hello from GitHub Actions!"
    }
    
    # เซฟผลลัพธ์เป็น JSON
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ Script completed successfully!")
    print("📄 Result saved to result.json")
    
    # แสดงผลลัพธ์
    print("\n📊 Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
