# Phase 1 Acceptance Criteria

Phase 1 จะถือว่าเสร็จเมื่อ:

- ติดตั้งแบบ editable ได้ด้วย `pip install -e .[dev]`
- รัน `codefind --help` ได้
- รัน `codefind find "login" .` ได้
- Output มี file path และ line number
- Output มี context 3 บรรทัดก่อน/หลัง
- ข้าม ignored directories ได้
- ไม่ crash เมื่ออ่านไฟล์ binary/permission error
- มี unit tests อย่างน้อย 4 cases
- `pytest` ผ่านทั้งหมด
