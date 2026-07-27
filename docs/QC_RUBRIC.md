# QC_RUBRIC — Grill 100 คะแนน

ที่มา: ChatGPT Design System Part 4 · ปรับ wording ให้ทีมใช้ซ้ำได้

## เกณฑ์ผ่าน

- **≥ 85 / 100** = ผ่านไป Export / ส่ง  
- **&lt; 85** = แก้ แล้ว grill ใหม่  
- โดน **Auto-reject** = ตกทันที แม้คะแนนรวมสูง

## 10 หมวด × 10 คะแนน

| หมวด | ถาม | 10 | 5 | 0–3 |
|---|---|---|---|---|
| Hook | 3s แรกหยุดนิ้ว? | อยากดูต่อทันที | ธรรมดา | เลื่อนผ่าน |
| Luxury | แบรนด์ vs ตลาดนัด? | premium | กลาง | ขายของโจ่ง |
| Product | เห็นทรง/สี/วัสดุ? | ชัด | พอ | กระเป๋าไม่ชัด |
| Story | ไหลหรือสะดุด? | เรื่องเดียว | สะดุดบ้าง | สลับสุ่ม |
| Variety | close/med/lifestyle/detail? | ครบสมดุล | ขาด 1 | ซ้ำมุมเดียว |
| Rhythm | จังหวะมีขึ้นลง? | ดี | แบนเล็กน้อย | ยาวเท่ากันหมด |
| Text | อ่านง่าย ไม่บัง? | หรู ชัด | เยอะไป | เต็มจอ/บังของ |
| Color | สม่ำเสมอ? | วันเดียว | เพี้ยนบ้าง | คนละวัน |
| Audio | VO/BGM รับใช้ภาพ? | ลงตัว | เพลงดังไป | แตก/กลบ |
| CTA | รู้ว่าทำอะไรต่อ? | ชัด อ่อนหรู | คลุมเครือ | ไม่มี |

### แผ่นคะแนน

```
Hook             __/10
Luxury           __/10
Product          __/10
Story            __/10
Variety          __/10
Rhythm           __/10
Typography       __/10
Color            __/10
Audio            __/10
CTA              __/10
---------------------
TOTAL            __/100
PASS (≥85)?      Y/N
AUTO-REJECT?     Y/N — reason:
```

## Auto-reject (ทันที)

- Export แนวนอน / สัดส่วนผิด  
- กระเป๋าไม่ชัดทั้งคลิป  
- Logo หรือสินค้าโดนตัดพัง  
- Text โดน TikTok UI  
- Hero เบลอ  
- สีสินค้าเพี้ยนชัด  
- จบไม่มี CTA (ถ้านโยบายร้านต้องมี)  
- Black frame  
- เสียงแตก (ถ้ามี audio track)  
- FPS พัง ภาพกระตุก  

## ข้อผิดพลาดยอดฮิต (แก้ยังไง)

| ผิด | แก้ |
|---|---|
| เปิดนานไม่เห็นของ | เห็นกระเป๋าใน 1s |
| ทุกช็อตยาวเท่ากัน | ผสม fast/med/slow |
| Text เต็มจอ | ≤3–5 บรรทัดทั้งคลิป |
| Macro ล้น | กลับ hero บ่อยขึ้น |
| ไม่มี lifestyle | ใส่ wear/walk |
| Detail แล้วไม่กลับ hero | ปิดด้วย packshot |
| เพลงกลบ VO | ลด BGM |
| Transition ทุกคัท | hard cut เป็นหลัก |
| สีเปลี่ยนทุกช็อต | grade ชุดเดียว |
| CTA ตะโกน | โทนหรู อ่อน |

## ไฟล์ QC.md ต่อจ็อบ

```markdown
# QC — {SKU} — {version}
date:
reviewer: human | ai | both
total: /100
pass: true|false
auto_reject: []
scores:
  hook: 
  luxury: 
  ...
notes:
  - 
fixes_required:
  - 
```
