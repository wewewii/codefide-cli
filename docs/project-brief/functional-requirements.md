# Functional Requirements

## FR-001 Search Keyword
ผู้ใช้สามารถค้นหา keyword ใน directory ได้ผ่าน CLI

```bash
codefind "login" .
```

## FR-002 Recursive Directory Search
ระบบต้องค้นหาทุกไฟล์ภายใต้ directory ที่กำหนดแบบ recursive

## FR-003 Default Ignore Directories
ระบบต้องข้าม directory ที่ไม่ควรค้นหาโดย default เช่น `.git`, `node_modules`, `dist`, `build`, `venv`, `.venv`, `__pycache__`

## FR-004 Extension Filter
ผู้ใช้สามารถกำหนด extension ที่ต้องการค้นหาได้

```bash
codefind "login" . --ext py,ts,tsx
```

## FR-005 Context Output
ระบบต้องแสดงบรรทัดที่ match พร้อม context ก่อนและหลัง โดย default คือ 3 บรรทัดก่อนและ 3 บรรทัดหลัง

## FR-006 Highlight Keyword
ระบบต้อง highlight keyword ที่ match ใน terminal

## FR-007 Summary
ระบบต้องแสดงจำนวน matches และจำนวน files ที่พบ

## FR-008 Open Editor
ผู้ใช้สามารถเปิดผลลัพธ์ไปยัง editor ได้

```bash
codefind "login" . --open vim
codefind "login" . --open code
```

## FR-009 Case Sensitive Option
ผู้ใช้สามารถเลือกค้นหาแบบ case-sensitive ได้

## FR-010 Regex Option
ผู้ใช้สามารถค้นหาด้วย regular expression ได้
