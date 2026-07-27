# วิธีขึ้น GitHub (public) — รอบเดียว

เครื่องนี้มี `gh` แบบ portable แล้ว แต่**ยังไม่ได้ login**

## 1) Login (รันครั้งเดียวบนเครื่อง)

PowerShell:

```powershell
& "$env:TEMP\gh-cli\bin\gh.exe" auth login
```

เลือก: GitHub.com → HTTPS → login ผ่าน browser  
(หรือวาง Personal Access Token ที่มีสิทธิ์ `repo`)

## 2) สร้าง repo public + push

```powershell
cd "C:\Users\Administrator\Documents\Obsidian Vault\20_Projects\bag-tiktok-studio"
& "$env:TEMP\gh-cli\bin\gh.exe" repo create bag-tiktok-studio --public --source=. --remote=origin --push --description "TikTok Shop bag video creative OS — DESIGN + 5-team pipeline"
```

## 3) ตรวจ

เปิด `https://github.com/<username>/bag-tiktok-studio`

## โคลนลง mini PC

```powershell
git clone https://github.com/<username>/bag-tiktok-studio.git
cd bag-tiktok-studio
# เปิดใน Grok แล้ว: อ่าน skill/SKILL.md
```

## ถ้าไม่อยากใช้ gh

1. สร้าง repo ว่างชื่อ `bag-tiktok-studio` แบบ Public บน github.com  
2. แล้ว:

```powershell
cd "C:\Users\Administrator\Documents\Obsidian Vault\20_Projects\bag-tiktok-studio"
git remote add origin https://github.com/<username>/bag-tiktok-studio.git
git push -u origin main
```
