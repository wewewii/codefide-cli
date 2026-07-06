# Phase 2 Task Breakdown - Robust Search

## Goal
ทำให้ search ใช้งานจริงกับ project ใหญ่ขึ้นได้ดีขึ้น

## Tasks

### CF-101 Add `--ext`
รองรับ extension filter เช่น `--ext py,ts,tsx`

### CF-102 Add `--ignore`
เพิ่ม custom ignore directories จาก user

### CF-103 Add `--context`
ปรับจำนวน context lines ได้

### CF-104 Improve Binary Detection
เพิ่ม heuristic เพื่อตรวจไฟล์ binary ก่อนอ่าน

### CF-105 Add Max File Size
เพิ่ม `--max-file-size` เพื่อ skip ไฟล์ใหญ่เกินกำหนด

### CF-106 Improve Error Handling
เก็บ skipped file count และแสดง warning summary แบบไม่รก

### CF-107 Add More Tests
เพิ่ม tests สำหรับ extension, ignore, large file และ unreadable file
