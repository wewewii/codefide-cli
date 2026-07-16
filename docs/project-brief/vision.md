# Vision

CodeFind CLI คือเครื่องมือค้นหาข้อความใน project directory สำหรับ developer ที่ต้องการหาตำแหน่งของ keyword, config, function name, error message หรือ secret key อย่างรวดเร็ว โดยไม่ต้องเปิดไฟล์ทีละไฟล์

## Problem

Developer มักเสียเวลาในการค้นหา string จากหลายไฟล์ โดยเฉพาะ project ที่มี backend, frontend, config, scripts และเอกสารปนกัน การใช้ editor search ทำได้ดี แต่บางครั้งต้องการทำงานผ่าน terminal และต้องการ context ที่อ่านง่ายกว่า grep แบบ raw output

## Product Goal

สร้าง terminal tool ที่:

- ค้นหา keyword จาก directory แบบ recursive
- แสดง file path และ line number
- แสดง context รอบบรรทัดที่เจอ
- highlight คำที่ match
- เปิดไฟล์ไปแก้ต่อด้วย Vim, VS Code หรือ Antigravity ได้

## Non-goals

- ไม่ทำ VS Code Extension ในเวอร์ชันแรก
- ไม่ทำ semantic search/AI ในเวอร์ชันแรก
- ไม่แทนที่ ripgrep ในด้าน performance ระดับสูงสุด
- ไม่ index project ล่วงหน้าใน MVP
