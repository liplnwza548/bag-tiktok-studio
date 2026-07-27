---
sku: LNB017
shop: CALUOMATT.TH
angle: A2
recipe: A
target_duration_sec: 20.5
bgm: Video_Studio/input/bgm/ (pick soft minimal · vol 0.25)
vo: none
status: draft
mode: best_effort_low_luxury
model_lock: B
sources:
  - jobs/CALUOMATT.TH/LNB017/FOOTAGE.md
  - Video_Studio .../LNB017/_INDEX.md (เติม keep ที่ FOOTAGE ถูกตัด token)
date: 2026-07-28
planner: grok-team2
---

# EDIT_PLAN — LNB017 (best effort)

## Intent

| | |
|---|---|
| emotion | **Minimal / soft everyday** (ไม่ pretends หรูโรงแรม — ลดความคาดหวัง luxury 3/10) |
| one_message | **ใบเดียว ใส่ได้หลายทรง ใช้จริงทุกวัน** |
| angle | **A2** (ใส่จริง) + แทรกหลักฐาน open/inside เบาๆ (A3 รอง) |
| hero_shot | `LNB017-04.MOV` **1.0–2.5s** — ถือโชว์ด้านหน้าลายดอก เต็มใบ (AGY 9) |
| exit_frame | `LNB017-05.MOV` **135.0–137.5s** — ยกถือหูหิ้ว เต็มใบ (AGY 9) · packshot |
| model | **B เท่านั้น** (02–05) · **ห้าม** ตัดไป A (01, 06) ในคลิปนี้ — กันสลับนางแบบสุ่ม |

## ทำไมเลือกแบบนี้ (honesty)

FOOTAGE Gemini: luxury 3 · usability 4 · พื้นหลังรก/แสงอุ่น  
→ แผนนี้ **ไม่ใช่คลิปทอง** · เป็นสูตร “ขายการใช้งานจากของที่มี”  
→ ตัวหนังสือ + hard cut + grade ชุดเดียว ช่วยดึงขึ้นเล็กน้อย **ห้าม** ยัด transition/effect ถี่เพื่อกลบพื้นหลัง

คาด QC: Luxury/Color อาจต่ำ · เป้าผ่านได้ถ้า Product+Story+CTA แน่น · อาจ **&lt;85** — ใช้เป็นตัวอย่าง pipeline ไม่ใช่ส่งร้านทันที

---

## Keep pool ที่ใช้ในแผนนี้ (model B only)

| source | t_in–t_out | type | score src | เหตุผล |
|---|---|---|---|---|
| LNB017-04 | 1.0–6.0 | hero | AGY 9 | hook เห็นทรง+ลาย |
| LNB017-03 | 55.0–59.0 | wear | AGY 9 | สะพายไหล่ โพสพร้อม |
| LNB017-05 | 24.0–29.0 | open | AGY 9 | มือเปิดช่องหน้า |
| LNB017-02 | 51.0–55.0 | inside | AGY 8 | อ้าปากโชว์จุของ |
| LNB017-02 | 69.0–75.0 | wear | AGY 8 | สะพายข้าง lifestyle |
| LNB017-05 | 45.0–50.0 | hero | AGY 9 | breathing / จำใบ |
| LNB017-03 | 80.0–84.0 | wear | AGY 8 | หันข้าง+หน้า |
| LNB017-05 | 86.0–89.0 | inside | AGY 8 | ซับใน (สั้น) |
| LNB017-04 | 76.0–78.0 | wear | AGY 8 | สะพายหันข้าง |
| LNB017-05 | 135.0–140.0 | hero | AGY 9 | exit packshot |

**ตัดทิ้งทั้งคลิป:** junk ทุกตัว · 01/06 (model A) · ช่วงจัดสาย/แปลงทรง · ซูมป้ายเหลืองยาว (detail tag 18–25 บน 04) — เสีย luxury

---

## Timeline (~20.5s) · สูตร A ปรับ best-effort

| # | t_tl | dur | source_file | t_in | t_out | shot_type | purpose | text | transition |
|---|------|-----|-------------|------|-------|-----------|---------|------|------------|
| 1 | 0.0 | 1.5 | LNB017-04.MOV | 1.0 | 2.5 | hero_product | **hook** เห็นกระเป๋าทันที | — | hard |
| 2 | 1.5 | 1.8 | LNB017-03.MOV | 55.0 | 56.8 | hero_wear | ใส่จริง สะพายไหล่ | `ใบเดียวจบวัน` | hard |
| 3 | 3.3 | 1.5 | LNB017-05.MOV | 24.5 | 26.0 | hand_interaction | หลักฐานใช้ / เปิดช่อง | — | hard |
| 4 | 4.8 | 1.6 | LNB017-02.MOV | 51.5 | 53.1 | open_interior | จุของ / ข้างใน | — | hard |
| 5 | 6.4 | 2.2 | LNB017-02.MOV | 70.0 | 72.2 | hero_wear | lifestyle สะพายข้าง | — | hard |
| 6 | 8.6 | 1.4 | LNB017-05.MOV | 45.5 | 46.9 | hero_product | **breathing** จำทรง ไร้ text | — | hard |
| 7 | 10.0 | 2.0 | LNB017-03.MOV | 80.5 | 82.5 | hero_wear | หันข้างโชว์ลาย | `แมตช์ได้ทุกลุค` | hard |
| 8 | 12.0 | 1.4 | LNB017-05.MOV | 86.5 | 87.9 | open_interior | ซับในสั้น (อย่ายาว) | — | hard |
| 9 | 13.4 | 1.8 | LNB017-04.MOV | 76.0 | 77.8 | hero_wear | สะพายใช้งาน | — | hard |
| 10 | 15.2 | 2.0 | LNB017-03.MOV | 113.0 | 115.0 | hero_product | ถือหูหิ้ว ชัด | — | hard |
| 11 | 17.2 | 1.5 | LNB017-02.MOV | 128.0 | 129.5 | hero_product | ยกถือ ใกล้จบ | — | hard |
| 12 | 18.7 | 1.8 | LNB017-05.MOV | 135.5 | 137.3 | packshot | **exit + CTA** | `พิกัดในตะกร้า` | hard |

**รวม dur:** 1.5+1.8+1.5+1.6+2.2+1.4+2.0+1.4+1.8+2.0+1.5+1.8 = **20.5s**

### จังหวะ

- slow: #1, #6, #12  
- med: ที่เหลือ  
- **transition ทั้งหมด = hard** (0 soft) — พื้นหลังรก ยิ่งใส่ effect ยิ่งดูถูก  
- speed ทุกช็อต **1.0x**  
- Ken Burns: ได้เบา 1.0→1.05 เฉพาะ #1 และ #12 เท่านั้น

---

## Text plan (สูงสุด 3 บรรทัดเนื้อหา + โลโก้ถ้ามี)

| t | dur | content | style_note |
|---|-----|---------|------------|
| 1.6 | 1.6 | `ใบเดียวจบวัน` | กลางบน safe · ฟอนต์ไทยบาง–กลาง · ไม่เต็มจอ · ไม่ทับหน้า/กระเป๋า |
| 10.2 | 1.6 | `แมตช์ได้ทุกลุค` | เดียวกัน · fade in/out เบา |
| 19.0 | 1.5 | `พิกัดในตะกร้า` | ล่างกลาง (เหนือ UI TikTok) · CTA อ่อน |
| optional | ทั้งเรื่อง | `CALUOMATT` | มุมเล็ก 1 จุดท้าย 18.7–20.5 ถ้าแม่พิมพ์มีช่องแบรนด์ |

**ห้าม:** !! · ลดแรง · รายการ feature ยาว · ข้อความซ้อนเกิน 1 บรรทัดพร้อมกัน

---

## Audio plan

- footage_audio: **mute ทุกช็อต**
- bgm: เพลงมินิมอลเบาจาก `input/bgm/` · **volume 0.25** · คลุม 0–20.5s
- vo: **none** รอบนี้ (ไม่มี VO คนคู่ SKU) — ภาพ+ตัวหนังสือเล่าเอง
- duck: ไม่มี

---

## Color / polish

- grade_note: **ชุดเดียวทั้งคลิป** — ดัน exposure เล็กน้อย · ลด warm ส้ม · อย่าใส่ฟิลเตอร์คนละใบ  
- เป้าหมาย: “ถ่ายวันเดียวกัน” แม้พื้นหลังไม่คลีน  
- ห้าม: glitch, whoosh ทุกคัท, sticker, vignette หนา

---

## Resolve paths (เครื่องแม่)

ฐาน:

```
.../Video_Studio/input/footage/ฟุตเทจจริง/CALUOMATT.TH/LNB017/
  LNB017-02/LNB017-02.MOV
  LNB017-03/LNB017-03.MOV
  LNB017-04/LNB017-04.MOV
  LNB017-05/LNB017-05.MOV
```

Draft ชื่อแนะนำ: `01-LNB017-CALUOMATT-A-besteffort`

แม่พิมพ์ build (เมื่อทีม 3): snapshot โทนช้า/กลาง (A_medium หรือ D_slow) — **ไม่ใช้ C_hype**

---

## Expected weak points (บอกทีม 4 ล่วงหน้า)

1. Luxury / Color — พื้นหลังประตู/ม่าน/ชั้นของ  
2. Tag สินค้าอาจโผล่บางช็อต — ถ้าเจอตอนเปิด CapCut ให้ trim ในเฟรม  
3. ไม่มี walk outdoor — lifestyle จำกัดในห้อง  
4. อาจได้ QC **75–84** · ใช้เรียนรู้ pipeline ไม่ใช่ส่งทันที

---

## Human approval (ทีม 2 → คน)

- [ ] ยอมรับ model **B only** (ไม่ปน 01/06)
- [ ] ยอมรับโหมด **best effort** (ไม่ใช่คลิปทอง)
- [ ] hero #1 + exit #12 โอเค
- [ ] ข้อความ 3 บรรทัดโอเค / แก้คำ
- [ ] พร้อมให้ทีม 3 ประกอบ CapCut

**สถานะ:** `draft` — ตั้ง `approved_by_human` เมื่อติ๊กครบ

---

## บันทึกทีม 5 ( foreshadow )

ถ้า Lip บอก “พื้นหลังยังไม่ได้” → อย่า batch ต่อ · บรีฟถ่าย: พื้นเรียบสว่าง · ถอดป้าย · โพสค้างนิ่ง 2s ก่อนเปลี่ยนทรง
