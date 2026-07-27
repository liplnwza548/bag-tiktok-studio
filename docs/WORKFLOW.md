# WORKFLOW — 5 ทีม

## บทบาทคน vs AI

| งาน | คน (Lip) | AI |
|---|---|---|
| ถ่าย / คัดฟุตเทจใส่โฟลเดอร์ SKU | ✅ | — |
| วิเคราะห์ฟุตเทจ → FOOTAGE.md | อนุมัติเร็ว | ทีม 1 |
| ออกแบบ EDIT_PLAN | เคาะรอบแรก | ทีม 2 |
| ประกอบ CapCut | เปิดตรวจ | ทีม 3 |
| QC ก่อนส่ง | เกตสุดท้าย | ทีม 4 ช่วยคะแนน |
| บันทึกบทเรียน + คอมเมนต์ | พูดคอมเมนต์ | ทีม 5 จด |

## ขั้นทีละทีม

### 0. เตรียมโฟลเดอร์ (คน)

ดู `examples/folder_layout.md`

```
jobs/{SHOP}/{SKU}/
  raw/           # หลายไฟล์ฟุตเทจที่คัดแล้ว
  FOOTAGE.md     # ทีม 1
  EDIT_PLAN.md   # ทีม 2
  QC.md          # ทีม 4
  LESSONS.md     # ทีม 5
```

### 1. ทีมตา — Footage Analyzer

- อ่านทุกไฟล์ใน `raw/` (วิดีโอ) **ไม่ใช้เสียง**  
- เขียน `FOOTAGE.md` ตาม `schemas/FOOTAGE.schema.md`  
- พรอมต์: `prompts/footage_analyzer.md`  
- เครื่องมือ: Gemini API (video) หรือ AGY  

**เกตคน:** สแกน 30–60 วินาที — Hero ถูกไหม / junk หลุดไหม

### 2. ทีมดีไซน์ — Creative Planner

- อินพุต: `FOOTAGE.md` + `DESIGN.md` + มุมขาย A1/A2/A3  
- เอาต์พุต: `EDIT_PLAN.md`  
- ห้าม invent ช็อตที่ไม่มีใน FOOTAGE  

**เกตคน (รอบแรก):** แผนอ่านแล้ว “หรูและขาย” ไหม

### 3. ทีมประกอบ — CapCut Builder

- v1: คนหรือ AI ทำตาม EDIT_PLAN ใน CapCut / สคริปต์โรงงานเดิม  
- v2: map เข้า draft JSON (ยังไม่ ship ใน repo นี้)  
- เอาต์พุต: draft ชื่อชัด เช่น `{SKU}_v1`

### 4. ทีม Grill — QC

- เปิดคลิปจริง (หรือ export ชั่วคราว)  
- คะแนนตาม `QC_RUBRIC.md`  
- < 85 หรือโดน auto-reject → กลับทีม 2/3  
- พรอมต์ช่วย: `prompts/grill_reviewer.md`

### 5. ทีมบันทึก — Lessons

- ทุกครั้งที่คนคอมเมนต์ หรือ QC ตก เขียน 1 บล็อกใน `LESSONS.md`  
- รายการที่ซ้ำ ≥3 ครั้ง → เสนอแก้ DESIGN / schema / prompt  
- ห้ามเก็บโน้ตแล้วไม่เปลี่ยนกฎ

## คำสั่งสั้นๆ บน PowerShell (เป้าหมาย UX)

```text
อ่าน skill/SKILL.md
รันทีม 1 บน jobs/CALUOMATT/LNB017
```

```text
จาก FOOTAGE.md เขียน EDIT_PLAN สูตร A มุม A2
```

```text
grill คลิปนี้ตาม QC_RUBRIC แล้วเขียน QC.md
```

## ห้าม

- ข้ามทีม 1 ไปประกอบเลย  
- batch หลายสิบคลิปก่อนคลิปทอง + QC ผ่าน  
- ใส่ footage / API key เข้า git  
