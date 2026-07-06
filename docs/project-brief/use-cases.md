# Use Cases

## UC-001 Find Function Usage
Developer ต้องการหา function `login` ว่าถูกเรียกจากไฟล์ไหนบ้าง

```bash
codefind "login" .
```

## UC-002 Find Environment Variable
Developer ต้องการหาว่า `JWT_SECRET` ถูกใช้ที่ไหน

```bash
codefind "JWT_SECRET" ./backend
```

## UC-003 Search Only TypeScript Files
Developer ต้องการค้นหาเฉพาะ frontend

```bash
codefind "useAuth" ./frontend --ext ts,tsx
```

## UC-004 Search and Open in Vim
Developer ต้องการค้นหาแล้วเปิดไปแก้ทันที

```bash
codefind "TODO" . --open vim
```

## UC-005 Search Error Message
Developer เห็น error จาก logs แล้วต้องการหา source code ที่สร้าง error นั้น

```bash
codefind "invalid token" .
```
