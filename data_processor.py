#!/usr/bin/env python3
"""
ตัวอย่างไฟล์ Python สำหรับประมวลผลข้อมูล
เหมาะสำหรับรันบน GitHub Actions
"""

import json
import pandas as pd
import requests
from datetime import datetime, timedelta
import os

def fetch_api_data():
    """ดึงข้อมูลจาก API ตัวอย่าง"""
    print("🌐 Fetching data from API...")
    
    # ใช้ public API ตัวอย่าง
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
        response.raise_for_status()
        
        data = response.json()[:5]  # เอาแค่ 5 รายการ
        print(f"✅ Fetched {len(data)} records")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []

def process_data(data):
    """ประมวลผลข้อมูล"""
    print("🔄 Processing data...")
    
    if not data:
        return
    
    # สร้าง DataFrame
    df = pd.DataFrame(data)
    
    # เพิ่มคอลัมน์ใหม่
    df['processed_at'] = datetime.now().isoformat()
    df['title_length'] = df['title'].str.len()
    
    # กรองข้อมูล
    df_filtered = df[df['title_length'] > 20]
    
    print(f"📊 Processed {len(df_filtered)} records")
    return df_filtered

def save_results(df):
    """บันทึกผลลัพธ์"""
    print("💾 Saving results...")
    
    # บันทึกเป็น JSON
    result = {
        "timestamp": datetime.now().isoformat(),
        "total_records": len(df),
        "data": df.to_dict('records')
    }
    
    with open("processed_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # บันทึกเป็น CSV (ถ้ามี pandas)
    try:
        df.to_csv("processed_data.csv", index=False, encoding="utf-8")
        print("📄 Saved CSV file")
    except Exception as e:
        print(f"⚠️ Could not save CSV: {e}")
    
    print("✅ Results saved successfully")

def generate_summary():
    """สร้างสรุปผลการทำงาน"""
    summary = {
        "run_time": datetime.now().isoformat(),
        "environment": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") else "Local",
        "python_version": os.sys.version,
        "working_directory": os.getcwd(),
        "files_created": []
    }
    
    # เช็คไฟล์ที่สร้าง
    for file in ["processed_data.json", "processed_data.csv"]:
        if os.path.exists(file):
            summary["files_created"].append(file)
    
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("📋 Summary generated")

def main():
    """ฟังก์ชันหลัก"""
    print("=" * 60)
    print("🐍 Data Processor - GitHub Actions Edition")
    print("=" * 60)
    
    # ดึงข้อมูล
    data = fetch_api_data()
    
    # ประมวลผล
    if data:
        processed_df = process_data(data)
        
        # บันทึกผลลัพธ์
        save_results(processed_df)
    
    # สร้างสรุป
    generate_summary()
    
    print("\n🎉 Data processing completed!")

if __name__ == "__main__":
    main()
