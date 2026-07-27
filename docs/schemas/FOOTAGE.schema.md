# FOOTAGE.md schema (ทีมตา)

เขียนหนึ่งไฟล์ต่อหนึ่งโฟลเดอร์ SKU  
วิเคราะห์**ภาพอย่างเดียว** — ห้ามอ้างเสียงจากไฟล์

```markdown
---
sku: LNB017
shop: CALUOMATT
angle_hint: A2          # ถ้าเดาได้จากฟุตเทจ ไม่งั้น unknown
model_primary: A        # A | B | unknown
files_count: 8
analyzer: gemini
date: YYYY-MM-DD
---

# FOOTAGE — {SKU}

## Summary
- overall_luxury_potential: 1-10
- overall_usability: 1-10
- one_line: "..."
- recommended_angle: A1|A2|A3
- recommended_hero_file: filename
- recommended_hero_t: start_sec-end_sec
- blockers: []          # สิ่งที่ทำให้ตัดไม่ได้

## Models
- id: A
  appearance: "..."
  appears_in: [file1, file2]

## Files
### {filename}
- duration_sec:
- type_mix: [selfie_wear, product_hand, mixed, junk]
- lighting: soft daylight | indoor warm | harsh | mixed
- background: clean | busy | ugly
- stability: good | shaky
- color_cast: neutral | warm | cool | bad
- audio_policy: ignore
- segments:
  - t_in: 0.0
    t_out: 2.5
    shot_type: hero_wear | hero_product | macro_hardware | open_interior | hand_interaction | walk | detail_texture | packshot | junk | other
    score: 1-10
    model: A|B|none
    bag_visible: full|partial|none
    bag_clarity: sharp|ok|blur
    notes: "..."
    use: hook|body|cta|reject
    reject_reason: "" 

## Keep list (must)
- file: ...
  t_in-t_out: ...
  shot_type: ...
  score: ...

## Reject list
- ...

## Gaps (ถ่ายเพิ่มถ้าเป็นไปได้)
- ...
```

## กฎคะแนนช็อต

- ≥ 8: ใช้ hook / hero ได้  
- 6–7: body  
- &lt; 6 หรือ type=junk: reject  
- head/tail เตรียมตัว: reject แม้ภาพพอใช้  
