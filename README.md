# bag-tiktok-studio

**Creative Operating System** สำหรับคลิป TikTok Shop กระเป๋าแฟชั่นผู้หญิง  
เป้าหมาย: คนเดียวจัดโฟลเดอร์ → AI ทำงานตามทีม → เปิด CapCut ตรวจ 2 นาที → Export

> Public skeleton · เอกสาร + schema + skill ก่อน · ตัวประกอบ CapCut JSON ทยอยใส่

## ใคร / โทน (ล็อกแล้ว)

| | |
|---|---|
| กลุ่มเป้า | นักศึกษา 18–24 · ออฟฟิศ 25–35 (ไทย) |
| ช่อง | TikTok Shop แนวตั้ง 9:16 |
| โทน | **หรู คลีน พื้นหลังสวย** · ดูแพง ไม่ตะโกนเซลล์ |
| สินค้า | 1 โฟลเดอร์ = 1 SKU = 1 คลิป · ทุกใบใช้สูตรเดียวกัน |
| วัตถุดิบ | หลายไฟล์ · เซลฟี่ใส่ + มือ/สินค้า · **ไม่ใช้เสียงจากฟุตเทจ** |
| คน | เจ้าของคัดโฟลเดอร์ + เกตสุดท้าย · AI ลดงาน 4 คน |

## Pipeline (5 ทีม)

```
โฟลเดอร์ SKU (คุณจัด)
    ↓
[1] ตา          FOOTAGE.md      ← Gemini / AGY
    ↓
[2] ดีไซน์      EDIT_PLAN.md    ← DESIGN.md + recipe
    ↓
[3] ประกอบ      CapCut draft    ← builder (ทีหลัง)
    ↓
[4] Grill/QC    ≥85/100         ← rubric
    ↓
[5] บันทึก      LESSONS.md      ← คอมเมนต์คุณ + บั๊ก
    ↓
คุณ Export
```

รายละเอียด: [`docs/WORKFLOW.md`](docs/WORKFLOW.md) · ดีไซน์: [`docs/DESIGN.md`](docs/DESIGN.md)

## เริ่มบนเครื่องใหม่

```powershell
git clone https://github.com/<YOUR_USER>/bag-tiktok-studio.git
cd bag-tiktok-studio
# เปิดโฟลเดอร์นี้ใน Grok / Claude แล้วพิมพ์:
#   อ่าน skill/SKILL.md แล้วทำตาม workflow ทีม 1 จากโฟลเดอร์ฟุตเทจ ...
```

ยังไม่ต้อง `npm install` — เฟสนี้เป็นเอกสาร + schema

## โครงสร้าง

```
bag-tiktok-studio/
├── README.md
├── docs/
│   ├── DESIGN.md           # ระบบครีเอทีฟ + กฎหรู + QC
│   ├── WORKFLOW.md         # 5 ทีม ขั้นตอนคน/เครื่อง
│   ├── SALES_ANGLES.md     # 3 มุมขาย default
│   ├── QC_RUBRIC.md        # คะแนน 100 + auto-reject
│   └── schemas/
│       ├── FOOTAGE.schema.md
│       ├── EDIT_PLAN.schema.md
│       └── shot.example.json
├── prompts/
│   ├── footage_analyzer.md # พรอมต์ Gemini ทีมตา
│   └── grill_reviewer.md
├── skill/
│   └── SKILL.md            # ให้ AI บนเครื่องอ่านแล้วทำ
├── examples/
│   └── folder_layout.md
├── scripts/                # ว่าง — ใส่เครื่องมือทีหลัง
└── jobs/                   # งานต่อ SKU (gitignore output ใหญ่)
```

## แหล่งที่มา

- สเปกเจ้าของ (Lip) + แผนทีม 5 ชั้น  
- ChatGPT Design System **Part 4** (QC, กฎเหล็ก, factory pipeline) จาก inbox  
- หมายเหตุ: dump ที่มีเป็น Part 4 เป็นหลัก — ส่วน north star / timeline recipe ถูกรวมและเติมจากสเปกล็อกของเจ้าของใน `DESIGN.md`  
- **ยังไม่ใช่** CapCut JSON builder เต็มรูป (ต้อง map effect/text id บนเครื่อง)

## สิ่งที่ repo นี้ยังไม่ทำ

- Export / โพสต์ให้อัตโนมัติ  
- รับประกันว่า ChatGPT cloud = draft บน CapCut Desktop เครื่องคุณ  
- เก็บฟุตเทจหรือ API key ใน git  

## License

MIT — ใช้เอง โคลน แก้ได้
