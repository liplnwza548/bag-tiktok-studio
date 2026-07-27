# scripts/

## พร้อมใช้

### `analyze_footage.py` — ทีม 1 (Gemini)

```powershell
python scripts/analyze_footage.py `
  --sku-dir "PATH\ฟุตเทจจริง\CALUOMATT.TH\LNB017" `
  --shop CALUOMATT.TH `
  --sku LNB017
```

- อ่านคีย์จาก `GEMINI_API_KEY` หรือ vault `SECRET.md` (บรรทัด Google Gemini API Key)  
- สร้าง proxy เบา (540p / 2fps / ไม่มีเสียง) แล้วส่ง **inline video** เข้า Gemini  
- หมายเหตุ: คีย์แบบ `AQ.*` บางตัว **File API upload ไม่ผ่าน** แต่ generateContent + inline ใช้ได้  
- เอาต์พุต: `jobs/{shop}/{sku}/FOOTAGE.md`

ตัวอย่างรันสำเร็จ: `jobs/CALUOMATT.TH/LNB017/FOOTAGE.md` (2026-07-28)

### `build_from_edit_plan.py` — ทีม 3 (CapCut)

```powershell
python scripts/build_from_edit_plan.py `
  --plan jobs/CALUOMATT.TH/LNB017/EDIT_PLAN.md `
  --snapshot A_medium `
  --name 01-LNB017-CALUOMATT-A-besteffort `
  --to-capcut
```

- โคลน snapshot จาก Video_Studio · multi-source ตาม timeline · mute · BGM 0.25  
- ต้อง `status: approved_by_human` ใน EDIT_PLAN  
- ตัวอย่างสำเร็จ: CapCut draft `01-LNB017-CALUOMATT-A-besteffort`

## คิวถัดไป

- `qa_scorecard.py` — ทีม 4 Grill  
- ปรับ text บน timeline ตาม t จริง (ตอนนี้ set-text ตามลำดับกล่อง)

