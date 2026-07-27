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

## คิวถัดไป

- `edit_plan_from_footage.py` — ทีม 2  
- เชื่อม CapCut builder ตาม `docs/CAPCUT_BUILD_SPEC.md`  
- `qa_scorecard.py` — ทีม 4  

