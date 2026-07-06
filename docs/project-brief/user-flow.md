# User Flow

## Basic Search Flow

1. User เปิด terminal ที่ root project
2. User รัน `codefind "keyword" .`
3. CLI validate keyword และ path
4. Scanner เดินไฟล์แบบ recursive
5. Scanner ข้าม ignored directories
6. Scanner อ่านไฟล์ text candidate
7. Scanner คืน matches
8. Formatter แสดง path, line number, context และ summary

## Open Editor Flow

1. User รัน `codefind "keyword" . --open vim`
2. CLI แสดงผลลัพธ์ทั้งหมด
3. ถ้ามี match เดียว เปิดไฟล์ทันที
4. ถ้ามีหลาย match ให้ user เลือกหมายเลข
5. Opener สร้าง command ตาม editor
6. CLI เรียก editor ผ่าน subprocess
