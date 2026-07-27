# EDIT_PLAN.md schema (ทีมดีไซน์)

อินพุตบังคับ: `FOOTAGE.md` + `docs/DESIGN.md`  
ห้ามใส่ช็อตที่ไม่มีใน Keep list

```markdown
---
sku: LNB017
shop: CALUOMATT
angle: A2
recipe: A              # A luxury-slow | B luxury-snappy
target_duration_sec: 20
bgm: TBD
vo: none | path
status: draft | approved_by_human
---

# EDIT_PLAN — {SKU}

## Intent
- emotion: Elegant | Minimal | ...
- one_message: "..."
- hero_shot: file + t_in-t_out
- exit_frame: file + t_in-t_out

## Timeline
| # | t_timeline | dur | source_file | t_in | t_out | shot_type | purpose | text | transition |
|---|------------|-----|-------------|------|-------|-----------|---------|------|------------|
| 1 | 0.0 | 1.4 | a.mp4 | 3.5 | 4.9 | hero_wear | hook | — | hard |
| 2 | ... | | | | | | | | |

## Text plan
| t | dur | content | style_note |
|---|-----|---------|------------|

## Audio plan
- footage_audio: mute all
- bgm: ...
- vo: ...

## Color
- grade_note: single look, clean luxury

## Human approval
- [ ] hero ok
- [ ] angle ok
- [ ] no random model switch
- [ ] ready for CapCut build
```
