# Phase 1 Task Breakdown - MVP CLI

## Goal
ทำให้ CLI ค้นหา keyword ใน directory ได้จริง พร้อม output file path, line number, context และ summary

## Tasks

### CF-001 Initialize Project
- Priority: P0
- Owner: Solo Developer
- Estimate: 0.5 day
- Deliverables: `pyproject.toml`, `src/codefind`, `tests`, `README.md`
- Acceptance Criteria:
  - `pip install -e .[dev]` ผ่าน
  - `codefind --help` ทำงาน
  - `pytest` ผ่าน

### CF-002 Implement CLI Arguments
- Priority: P0
- Owner: Solo Developer
- Estimate: 0.5 day
- Deliverables: `src/codefind/main.py`
- Acceptance Criteria:
  - รับ `keyword` และ `path`
  - validate path มีอยู่จริงและเป็น directory
  - แสดง error ชัดเจนเมื่อ input ผิด

### CF-003 Implement File Traversal
- Priority: P0
- Owner: Solo Developer
- Estimate: 1 day
- Deliverables: `iter_files()`
- Acceptance Criteria:
  - เดินไฟล์ recursive ได้
  - ข้าม `.git`, `node_modules`, `dist`, `venv`, `.venv`

### CF-004 Implement Keyword Search
- Priority: P0
- Owner: Solo Developer
- Estimate: 1 day
- Deliverables: `search_directory()`
- Acceptance Criteria:
  - เจอ keyword แบบ case-insensitive by default
  - เก็บ file path, line number, matched line
  - ไม่ crash เมื่อเจอไฟล์อ่านไม่ได้

### CF-005 Implement Context Lines
- Priority: P0
- Owner: Solo Developer
- Estimate: 0.5 day
- Acceptance Criteria:
  - default context = 3
  - รวมบรรทัดที่ match ตรงกลางเมื่อเป็นไปได้
  - handle กรณี match อยู่ต้นไฟล์หรือท้ายไฟล์

### CF-006 Implement Terminal Output
- Priority: P0
- Owner: Solo Developer
- Estimate: 1 day
- Deliverables: `formatter.py`
- Acceptance Criteria:
  - แสดง format `path:line`
  - แสดง marker `>` ที่บรรทัด match
  - highlight keyword
  - แสดง summary

### CF-007 Add Basic Tests
- Priority: P0
- Owner: Solo Developer
- Estimate: 1 day
- Acceptance Criteria:
  - test match
  - test no match
  - test context
  - test ignore directory
