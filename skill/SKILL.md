---
name: bag-tiktok-studio
description: โรงงานคลิป TikTok Shop กระเป๋าโทนหรู — ทีมตา → ดีไซน์ → ประกอบ → grill → บันทึก
---

# Skill: bag-tiktok-studio

## เมื่อไหร่ใช้สกิลนี้

- ผู้ใช้ชี้โฟลเดอร์ฟุตเทจ SKU แล้วให้ช่วยวิเคราะห์ / วางแผนตัด / QC
- ติดตั้งหรือทำงานบน clone ของ repo นี้

## อ่านก่อนลงมือ (บังคับ)

1. `docs/DESIGN.md`
2. `docs/WORKFLOW.md`
3. schema ที่เกี่ยวกับงาน (`FOOTAGE` / `EDIT_PLAN` / `QC_RUBRIC`)

## กฎเหล็ก

- ไม่ใช้เสียงจากฟุตเทจ
- 1 โฟลเดอร์ = 1 SKU = 1 คลิป
- เลือก Hero ก่อน timeline
- ไม่ batch ใหญ่ก่อนคลิปตัวอย่างผ่าน QC
- ไม่ commit ฟุตเทจ / API key
- ไม่อ้างว่า CapCut draft เสร็จถ้ายังเปิดใน CapCut Desktop ไม่ได้

## คำสั่งที่รองรับ

### ทีม 1 — วิเคราะห์ฟุตเทจ

```
รันทีมตาบน <path-to-sku-folder>
```

→ เขียน `FOOTAGE.md` ในโฟลเดอร์นั้นตาม schema  
→ ใช้ `prompts/footage_analyzer.md` + Gemini ถ้ามีวิดีโอ

### ทีม 2 — แผนตัด

```
เขียน EDIT_PLAN จาก FOOTAGE.md มุม A2 สูตร A
```

→ อ่าน FOOTAGE + DESIGN → `EDIT_PLAN.md`  
→ ช็อตต้องมาจาก keep list เท่านั้น

### ทีม 4 — Grill

```
grill <video-or-draft-notes>
```

→ `QC.md` คะแนน 100

### ทีม 5 — บันทึก

```
จดบทเรียน: <คอมเมนต์ผู้ใช้>
```

→ ต่อท้าย `LESSONS.md` วันที่ + ผลกระทบต่อ DESIGN/prompt

## สิ่งที่ยังไม่ทำในสกิลนี้ (v1)

- เขียน CapCut `draft_content.json` อัตโนมัติเต็มรูป  
- Export / อัปโหลด TikTok  

ถ้าผู้ใช้ขอส่วนนี้: อธิบายขอบเขต แล้วช่วยทำด้วยมือตาม EDIT_PLAN หรือชี้ไป Video_Studio scripts ถ้ามีบนเครื่อง
