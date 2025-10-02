# Kintone Status Capture Bot

Python bot สำหรับ capture หน้าจอแบบ print view จาก Kintone records และบันทึกเป็นไฟล์รูปภาพ โดยจะเลื่อนลงล่างสุดก่อน capture เพื่อให้ได้ข้อมูลครบถ้วน

## คุณสมบัติ

- Login เข้า Kintone ผ่าน browser automation (Selenium)
- เปิดหน้า print view ของแต่ละ record แบบ sequential (record ID 1, 2, 3, ...)
- ตรวจจับและปิด error dialogs อัตโนมัติ
- เลื่อนลงล่างสุดของหน้าก่อน capture
- บันทึก screenshot เป็นไฟล์ `record_{ID}.png`
- หยุดอัตโนมัติเมื่อเจอ 5 records ติดกันที่ไม่มีข้อมูล

## การติดตั้ง

### 1. Clone repository
```bash
git clone <repository-url>
cd kintone-capture-status
```

### 2. สร้าง virtual environment (แนะนำ)
```bash
python -m venv venv
source venv/bin/activate  # สำหรับ macOS/Linux
# หรือ
venv\Scripts\activate  # สำหรับ Windows
```

### 3. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า environment variables
สร้างไฟล์ `.env` โดย copy จาก `.env.example`:
```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env` และกรอกข้อมูล:
```env
KINTONE_DOMAIN=your-domain.kintone.com
KINTONE_USERNAME=your-username
KINTONE_PASSWORD=your-password
KINTONE_APP_ID=your-app-id
```

**หมายเหตุ:**
- `KINTONE_DOMAIN` ไม่ต้องใส่ `https://` หรือ `/` ท้าย (เช่น `demo.kintone.com`)
- `KINTONE_APP_ID` ใส่เป็นตัวเลข ID ของ app (เช่น `20`)

## วิธีใช้งาน

### รัน bot
```bash
# Activate virtual environment (ถ้ายังไม่ได้ activate)
source venv/bin/activate

# รัน script
python main.py
```

### ผลลัพธ์
- Screenshot จะถูกบันทึกในโฟลเดอร์ `screenshots/`
- ชื่อไฟล์: `record_{ID}.png` (เช่น `record_1.png`, `record_2.png`)
- หาก record ไม่มีข้อมูล จะไม่มี screenshot ของ record นั้น
- หากมี error dialog: screenshot จะถูกบันทึกเป็น `record_{ID}_error.png`

### การหยุด bot
- กด `Ctrl+C` เพื่อหยุดการทำงาน
- Bot จะหยุดอัตโนมัติเมื่อเจอ 5 records ติดกันที่ไม่มีข้อมูล

## โครงสร้างโปรเจค

```
kintone-capture-status/
├── .env                    # Environment variables (ไม่ commit)
├── .env.example           # ตัวอย่าง environment variables
├── .gitignore             # Git ignore rules
├── CLAUDE.md              # คู่มือสำหรับ Claude Code
├── README.md              # คู่มือการใช้งาน
├── requirements.txt       # Python dependencies
├── main.py                # Main script (ใช้ไฟล์นี้)
├── browser_automation.py  # Browser automation logic
├── kintone_client.py      # Kintone API client (ไม่ได้ใช้ในเวอร์ชันปัจจุบัน)
└── screenshots/           # Output directory (ไม่ commit)
```

## การทำงานของ Bot

1. **Login**: เปิด browser และ login เข้า Kintone ด้วย username/password
2. **Loop Records**: เริ่มจาก record ID = 1 และวนไปเรื่อยๆ
3. **Open Print View**: เปิด URL แบบ `https://{domain}/k/{app_id}/print?record={id}`
4. **Error Handling**: ตรวจสอบ error dialogs และปิดถ้ามี
5. **Scroll & Capture**: เลื่อนลงล่างสุด แล้ว capture screenshot
6. **Save**: บันทึกเป็น `record_{ID}.png`
7. **Next**: ไป record ถัดไป จนกว่าจะเจอ 5 records ที่ไม่มีข้อมูลติดกัน

## Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (จะติดตั้งอัตโนมัติผ่าน webdriver-manager)
- Kintone account พร้อม username/password

## Troubleshooting

### Browser ไม่เปิด
- ตรวจสอบว่าติดตั้ง Google Chrome แล้ว
- ลองรัน `pip install --upgrade selenium webdriver-manager`

### Login ไม่สำเร็จ
- ตรวจสอบ username/password ในไฟล์ `.env`
- ตรวจสอบว่า domain ถูกต้อง (ไม่มี https:// หรือ /)

### Screenshot ว่างเปล่า
- เพิ่มเวลารอใน `time.sleep()` ในไฟล์ `main.py`
- ลองปิด headless mode โดยแก้ `headless=False` ใน `main.py`

## License

MIT
