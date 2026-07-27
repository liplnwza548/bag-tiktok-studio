# CAPCUT_BUILD_SPEC v1

> Engineering handoff: จาก EDIT_PLAN.md → CapCut Desktop draft  
> เติมจากเครื่อง Lip (2026-07-28) + OPEN_QUESTIONS ที่ปิดแล้ว

---

## 0. Locked answers (OPEN_QUESTIONS)

| # | คำถาม | คำตอบ |
|---|---|---|
| A | CapCut Desktop | **9.1.0.3879** (มี 9.0.0.3858 ด้วย) · path `AppData\Local\CapCut` |
| B | FPS export | **30** (default) |
| C | ความยาว default | **20–22s** สูตร A (หรูช้า) · สูตร B 15–18s ทีหลัง |
| D | Text template | **มีคลังบนเครื่อง** (Video_Studio `text_template.py` / bank ~58) · map id จาก draft ตัวอย่าง · ไทยใช้ฟอนต์ใน `font_bank` |
| E | BGM | โฟลเดอร์ `Video_Studio/input/bgm/` (หลายไฟล์ .mp3) · ระดับดังเป้าหมาย **~25%** (0.25) ตามโรงงานเดิม |
| F | VO | **คนจริงเท่านั้น** · ห้าม AI voice · mute เสียงฟุตเทจ |
| G | ชื่อไฟล์ฟุตเทจ | `{SKU}-{NN}.MOV` ในโฟลเดอร์ย่อยชื่อเดียวกัน เช่น `LNB017/LNB017-01/LNB017-01.MOV` |
| H | โฟลเดอร์ | `jobs/{SHOP}/{SKU}/raw|FOOTAGE|EDIT_PLAN|QC` · วัตถุดิบหลักอยู่ `Video_Studio/input/footage/ฟุตเทจจริง/{SHOP}/{SKU}/` |
| I | Random recipe | **v1 ไม่ random** · สูตร A คงที่ |
| J | Hero approve | **v1 รอคน** หลัง FOOTAGE.md · ทีหลังค่อย auto ถ้า QC ดี |

---

## 1. Canvas / timeline

| พารามิเตอร์ | ค่า |
|---|---|
| resolution | 1080 × 1920 |
| fps | 30 |
| duration | ตาม EDIT_PLAN (`target_duration_sec` 20–22) |
| video tracks | หลัก 1 (สินค้า/wear) · อย่าเปิด multi-timeline ผิดสำเนา |
| audio | BGM 1 track · VO 0–2 tracks (เกยได้) · **footage volume = 0** |

### กับดักเครื่องนี้ (บังคับ)

CapCut multi-timeline: ไฟล์จริงอาจอยู่ `Timelines/<GUID>/draft_content.json`  
เขียน root อย่างเดียวแล้วเปิดแอป → งานถูกทับ  
→ builder ต้อง `save_draft` ทุกสำเนา + verify หลังเขียน

---

## 2. Input contract (ก่อน build)

ต้องมีครบ:

1. `FOOTAGE.md` (ทีม 1) — keep list + hero  
2. `EDIT_PLAN.md` status `approved_by_human` (ทีม 2 + คน)  
3. path ไฟล์วิดีโอ resolve ได้บนเครื่อง  
4. BGM path (default จากคลัง)  
5. (optional) VO path คนจริง  

ขาดข้อ 2 → **ห้าม build**

---

## 3. Mapping EDIT_PLAN → CapCut segments

| EDIT_PLAN field | CapCut / JSON concept |
|---|---|
| `source_file` + `t_in`/`t_out` | video segment source_timerange (microseconds) |
| `dur` / timeline order | target_timerange ต่อเนื่อง |
| `transition: hard` | ไม่ใส่ transition object |
| `transition: soft` | ใส่ transition จากคลังที่ harvest แล้วเท่านั้น |
| `text` rows | text track / text_template apply + ฟอนต์ไทย |
| `bgm` | audio segment ยาวคลุม · volume ~0.25 |
| `vo` | audio segment(s) · เกยตาม VO overlap spec ถ้ามี |
| `grade_note` | ชุด effect เดียวซ้ำทุกช็อต (จาก snapshot แม่พิมพ์) |

### หน่วยเวลา

- เอกสารมนุษย์: **วินาที**  
- CapCut JSON: **ไมโครวินาที** (`sec * 1_000_000`)

### กฎ picks จาก DESIGN

- ห้ามใช้ segment ที่ FOOTAGE ติด `reject` / junk  
- ตัดหัว–ท้ายเตรียมตัวตาม keep list ไม่เดาเพิ่ม  
- 1 คลิป 1 นางแบบหลักตาม FOOTAGE `model_primary`

---

## 4. Template / DNA strategy

v1 build path (แนะนำ):

```
EDIT_PLAN + FOOTAGE
    → apply ลง snapshot แม่พิมพ์ที่ freeze แล้ว
      (โทนหรู: ช้า / medium — ไม่ใช้ hype ก่อนมีคลิปทอง)
    → แทน footage paths + source in/out ต่อช็อต
    → ใส่ text ตาม TEXT_PLAN
    → BGM 0.25 · mute video
    → เปิดใน CapCut ให้คน QC
```

**อย่า** สร้าง effect_id ใหม่จากชื่อในเอกสาร — ใช้ id จาก draft บนเครื่องนี้เท่านั้น

คลังอ้างอิงบนเครื่องแม่ (นอก repo นี้):

- `Video_Studio/templates/snapshot/*`
- `Video_Studio/scripts/build_from_snapshot.py` (single-source เดิม)
- multi-source: `build_from_shot_bank.py` (แล็บ) — ต้องผูก EDIT_PLAN ทีหลัง

---

## 5. Builder agent steps (algorithm)

```
1. load EDIT_PLAN.md + FOOTAGE.md
2. assert human approval flag
3. resolve each source_file → absolute path
4. pick base template snapshot (config: luxury_default)
5. clone snapshot → drafts/{SKU}_vN/
6. for each timeline row:
     create/replace video segment
     set source range, speed 1.0
     mute
     apply grade stack from template (ไม่สุ่ม)
7. apply text layers (font must support Thai)
8. place BGM full length vol 0.25
9. place VO if any
10. save all timeline copies + verify checksum/sync
11. write BUILD_REPORT.md (paths, shot count, duration)
12. stop for human CapCut open + Grill (ทีม 4)
```

---

## 6. Machine QA before human

| ตรวจ | ผ่านเมื่อ |
|---|---|
| path ไฟล์ | ทุก source มีจริง |
| duration | รวม ≈ target ±1.5s |
| junk | ไม่มี t_in/out จาก reject list |
| audio | ไม่มี volume ฟุตเทจ > 0 |
| text Thai | ฟอนต์รองรับ glyph |
| multi-timeline | root == Timelines/* content hash |
| canvas | 1080x1920 @ 30 |

---

## 7. Naming drafts

```
{index}-{SKU}-{SHOP_SHORT}-{recipe}
ตัวอย่าง: 01-LNB017-CALUOMATT-A
```

---

## 8. Out of scope v1

- Auto export  
- Upload TikTok  
- Random recipe engine  
- เดา flip / กลับด้าน AI  
- สร้าง text_template ใหม่ทั้งก้อนบน cloud CapCut  

---

## 9. Next implementation tickets

1. `scripts/edit_plan_to_shotlist.py` — parse EDIT_PLAN → JSON shotlist  
2. เชื่อม shotlist → `build_from_shot_bank` หรือ builder ใหม่ใน repo นี้ (copy logic ไม่ลาก footage เข้า git)  
3. harvest 1 แม่พิมพ์หรูจาก draft ที่คนเคาะ → `templates/` เฉพาะ metadata + id map  
4. `scripts/qa_draft_machine.py` — checklist ข้อ 6  
