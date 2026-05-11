#!/usr/bin/env python3
"""
ไฟล์ตั้งค่าสำหรับโปรเจกต์ GitHub Actions
"""

import os
from datetime import datetime

class Config:
    """คลาสสำหรับเก็บค่าตั้งค่า"""
    
    # ตั้งค่าสำหรับ GitHub Actions
    IS_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS", "false") == "true"
    
    # ข้อมูลเวลา
    NOW = datetime.now()
    TIMESTAMP = NOW.isoformat()
    
    # ตั้งค่า API
    API_TIMEOUT = 10
    REQUEST_DELAY = 1
    
    # ตั้งค่าไฟล์
    OUTPUT_DIR = "output" if not IS_GITHUB_ACTIONS else "."
    
    # ตั้งค่า scraping
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    MAX_LINKS = 10
    
    # ตั้งค่า environment
    if IS_GITHUB_ACTIONS:
        print("🤖 Running on GitHub Actions")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🏢 Repository: {os.environ.get('GITHUB_REPOSITORY', 'Unknown')}")
    else:
        print("🏠 Running locally")
        print(f"📁 Working directory: {os.getcwd()}")

def get_env_info():
    """ดึงข้อมูล environment"""
    return {
        "is_github_actions": Config.IS_GITHUB_ACTIONS,
        "timestamp": Config.TIMESTAMP,
        "working_directory": os.getcwd(),
        "python_version": os.sys.version,
        "platform": os.sys.platform
    }

def setup_output_directory():
    """สร้างโฟลเดอร์ output ถ้าจำเป็น"""
    if not os.path.exists(Config.OUTPUT_DIR) and not Config.IS_GITHUB_ACTIONS:
        os.makedirs(Config.OUTPUT_DIR)
        print(f"📁 Created output directory: {Config.OUTPUT_DIR}")

if __name__ == "__main__":
    # ทดสอบการทำงาน
    print("🔧 Testing Configuration")
    print("=" * 40)
    
    env_info = get_env_info()
    for key, value in env_info.items():
        print(f"{key}: {value}")
    
    setup_output_directory()
    print("✅ Configuration test completed")
