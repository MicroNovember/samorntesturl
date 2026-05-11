# การรัน Python บน GitHub Actions

## 📁 โครงสร้างไฟล์
```
github/
├── .github/
│   └── workflows/
│       └── run-python.yml     # Workflow file
├── example_script.py          # ตัวอย่างไฟล์ Python
├── requirements.txt           # Dependencies
└── README.md                  # ไฟล์นี้
```

## 🚀 วิธีใช้งาน

### 1. Push ขึ้น GitHub
```bash
git add .
git commit -m "Add GitHub Actions workflow for Python"
git push origin main
```

### 2. ดูผลลัพธ์
1. ไปที่แถบ **Actions** บน GitHub
2. เลือก workflow **Run Python Script**
3. ดู log และผลลัพธ์

### 3. รันเอง (Manual Run)
1. ไปที่หน้า Actions
2. เลือก **Run Python Script**
3. กดปุ่ม **Run workflow** ด้านขวา

## ⚙️ การตั้งค่า Workflow

### Trigger ที่ใช้ได้:
- `push`: รันตอน push code ขึ้น main/master
- `workflow_dispatch`: กดรันเองได้
- `schedule`: รันทุก 6 ชั่วโมง (cron: '0 */6 * * *')

### สิ่งที่ Workflow ทำ:
1. ✅ Checkout code
2. 🐍 Setup Python 3.10
3. 📦 Install dependencies (จาก requirements.txt)
4. 🏃 Run ไฟล์ Python ทั้งหมด (*.py)
5. 📤 Upload artifacts (ไฟล์ .json, .txt, .log)

## 📝 การเพิ่มไฟล์ Python

เพียงสร้างไฟล์ `.py` ในโปรเจกต์ และ push ขึ้น GitHub:
```python
# your_script.py
print("Hello from my script!")
```

Workflow จะรันไฟล์ Python ทั้งหมดในโฟลเดอร์โปรเจกต์อัตโนมัติ

## 🔧 การปรับแต่ง

### เปลี่ยน Python Version:
แก้ไฟล์ `.github/workflows/run-python.yml`:
```yaml
python-version: '3.11'  # เปลี่ยนเป็นเวอร์ชันที่ต้องการ
```

### เปลี่ยน Schedule:
```yaml
schedule:
  - cron: '0 */2 * * *'  # รันทุก 2 ชั่วโมง
```

### รันไฟล์เฉพาะ:
```yaml
- name: Run Python Script
  run: python your_specific_file.py
```

## 📦 Dependencies Management

เพิ่ม libraries ที่ต้องการใน `requirements.txt`:
```
requests>=2.31.0
pandas>=2.0.0
```

## 🎯 ตัวอย่างจากไฟล์ scanner.py

สำหรับโปรเจกต์ที่ต้องการ Selenium/Chrome:
```yaml
- name: Install Chrome and Driver
  run: |
    sudo apt-get update
    sudo apt-get install -y google-chrome-stable chromium-chromedriver
```

## 📊 ผลลัพธ์

- ดู log ในหน้า Actions
- ดาวน์โหลด artifacts จาก workflow run
- ไฟล์ผลลัพธ์จะถูกเซฟเป็น .json, .txt, .log

---

🎉 **พร้อมใช้งานแล้ว!** แค่ push ขึ้น GitHub ก็เริ่มรันได้เลย
