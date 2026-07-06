# Coding Standard

## Python

- ใช้ Python 3.11+
- ใช้ type hints ทุก public function
- function ควรสั้นและมีหน้าที่เดียว
- หลีกเลี่ยง side effects ใน scanner
- subprocess เรียกเฉพาะใน opener

## Naming

- function: `snake_case`
- dataclass: `PascalCase`
- constants: `UPPER_CASE`

## Error Handling

- CLI input error ให้ใช้ Typer error
- file read error ให้ skip ไม่ crash
- invalid regex ต้องแจ้ง user ชัดเจน

## Testing

- ทุก behavior หลักต้องมี unit test
- ไม่ทดสอบผ่าน project จริงใน unit test
- ใช้ `tmp_path` เพื่อสร้าง fixture files
