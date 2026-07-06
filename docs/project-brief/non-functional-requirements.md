# Non-functional Requirements

## Performance

- MVP ควรค้นหา project ขนาดเล็กถึงกลางได้ภายในเวลาไม่กี่วินาที
- ต้องไม่ crash เมื่อเจอไฟล์ binary หรือไฟล์ encoding แปลก
- ต้องไม่อ่าน directory ที่ ignore โดยไม่จำเป็น

## Reliability

- ถ้าอ่านไฟล์ไม่ได้ ให้ skip แทนที่จะหยุดโปรแกรม
- ถ้า path ไม่ถูกต้อง ต้องแจ้ง error ชัดเจน
- ถ้าไม่เจอ match ต้องแสดงข้อความที่เข้าใจง่าย

## Usability

- CLI help ต้องอ่านง่าย
- Output ต้องอ่านง่ายกว่า grep พื้นฐาน
- Default behavior ต้องใช้งานได้ทันทีโดยไม่ต้อง config

## Maintainability

- แยก module ชัดเจน: CLI, scanner, formatter, opener
- มี unit tests สำหรับ core search logic
- ใช้ type hints
- ใช้ ruff/mypy เพื่อคุมคุณภาพ

## Portability

- รองรับ macOS และ Linux เป็นหลัก
- Windows ยังไม่ใช่ priority ใน MVP แต่ไม่ควรออกแบบให้ปิดทาง
