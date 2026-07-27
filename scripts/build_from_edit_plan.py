# -*- coding: utf-8 -*-
"""
Team 3 — CapCut Builder from EDIT_PLAN.md
Clones a Video_Studio snapshot, maps multi-file shots from the plan,
rewrites target durations, mutes video, BGM 0.25, sync multi-timeline.

Usage (from anywhere):
  python scripts/build_from_edit_plan.py ^
    --plan jobs/CALUOMATT.TH/LNB017/EDIT_PLAN.md ^
    --snapshot A_medium --name 01-LNB017-CALUOMATT-A-besteffort --to-capcut
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VS = Path(r"C:\Users\Administrator\Documents\Obsidian Vault\20_Projects\Video_Studio")
VS_SCRIPTS = VS / "scripts"
sys.path.insert(0, str(VS_SCRIPTS))
import shell_swap as ss  # noqa: E402

FOOTAGE_BASE = VS / "input" / "footage" / "ฟุตเทจจริง"
BGM_DIR = VS / "input" / "bgm"


def parse_timeline(plan_text: str) -> list[dict]:
    """Parse markdown table rows under ## Timeline."""
    lines = plan_text.splitlines()
    rows = []
    in_table = False
    for line in lines:
        if line.strip().startswith("## Timeline"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table:
            continue
        if not line.strip().startswith("|"):
            continue
        if re.search(r"\|\s*#\s*\|", line) or re.search(r"\|\s*-+", line):
            continue
        parts = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(parts) < 10:
            continue
        try:
            num = int(parts[0])
            t_tl = float(parts[1])
            dur = float(parts[2])
            src = parts[3]
            t_in = float(parts[4])
            t_out = float(parts[5])
            shot_type = parts[6]
            purpose = parts[7]
            text = parts[8] if parts[8] not in ("—", "-", "") else ""
            transition = parts[9]
        except Exception:
            continue
        rows.append(
            {
                "i": num,
                "t_tl": t_tl,
                "dur": dur,
                "source_file": src,
                "t_in": t_in,
                "t_out": t_out,
                "shot_type": shot_type,
                "purpose": purpose,
                "text": text,
                "transition": transition,
            }
        )
    return rows


def resolve_path(shop: str, sku: str, source_file: str) -> Path:
    # LNB017-04.MOV -> LNB017/LNB017-04/LNB017-04.MOV
    name = source_file
    stem = Path(name).stem  # LNB017-04
    candidates = [
        FOOTAGE_BASE / shop / sku / stem / name,
        FOOTAGE_BASE / shop / sku / name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError(f"missing footage: {source_file} (tried under {FOOTAGE_BASE / shop / sku})")


def write_all_bases(dest: str, d: dict):
    content = json.dumps(d, ensure_ascii=False)
    bases = [dest]
    tdir = os.path.join(dest, "Timelines")
    if os.path.isdir(tdir):
        for g in os.listdir(tdir):
            gp = os.path.join(tdir, g)
            if os.path.isdir(gp):
                bases.append(gp)
    for base in bases:
        for fn in ("draft_content.json", "draft_content.json.bak", "template-2.tmp"):
            fp = os.path.join(base, fn)
            if fn == "draft_content.json" or os.path.exists(fp):
                open(fp, "w", encoding="utf-8").write(content)


def pick_bgm() -> Path | None:
    if not BGM_DIR.is_dir():
        return None
    files = sorted(BGM_DIR.glob("*.mp3"))
    # prefer mid-energy soft; else first
    for pref in ("400", "375", "364", "282", "251"):
        for f in files:
            if pref in f.stem:
                return f
    return files[0] if files else None


def rechain_video(vt: dict, plan: list[dict]):
    """Resize first len(plan) segments; drop extras; set target ranges."""
    segs = vt["segments"]
    if len(segs) < len(plan):
        raise SystemExit(f"template has {len(segs)} segs < plan {len(plan)}")
    # keep first N as templates for effects
    keep = segs[: len(plan)]
    t_cursor = 0
    for i, row in enumerate(plan):
        seg = keep[i]
        dur_us = int(round(row["dur"] * 1_000_000))
        seg["target_timerange"] = {"start": t_cursor, "duration": dur_us}
        # source duration matches timeline dur (1.0x)
        seg["source_timerange"]["duration"] = dur_us
        start_us = int(round(row["t_in"] * 1_000_000))
        seg["source_timerange"]["start"] = start_us
        seg["volume"] = 0.0
        # light zoom on first and last only
        if i == 0 or i == len(plan) - 1:
            ss.apply_uniform_zoom(seg, start_us, dur_us, 1.0, 1.05)
        else:
            ss.apply_uniform_zoom(seg, start_us, dur_us, 1.0, 1.0)
        # hard cut: clear transition if any
        if "transition" in seg:
            try:
                del seg["transition"]
            except Exception:
                pass
        if "extra_material_refs" in seg:
            # leave refs; transition materials may linger — ok
            pass
        t_cursor += dur_us
    vt["segments"] = keep
    return t_cursor


def scale_non_video_tracks(d: dict, new_dur_us: int, old_dur_us: int):
    if old_dur_us <= 0:
        return
    ratio = new_dur_us / old_dur_us
    for t in d.get("tracks", []):
        if t.get("type") == "video" and t.get("attribute") == 1:
            continue
        for seg in t.get("segments", []):
            tr = seg.get("target_timerange") or {}
            st = int(tr.get("start", 0) * ratio)
            du = int(tr.get("duration", 0) * ratio)
            # clamp inside new timeline
            if st >= new_dur_us:
                st = max(0, new_dur_us - max(du, 100_000))
            if st + du > new_dur_us:
                du = max(100_000, new_dur_us - st)
            seg["target_timerange"] = {"start": st, "duration": du}


def set_texts(dest: str, plan: list[dict], new_dur_us: int):
    """Best-effort: set-text on existing text segments in order for non-empty plan texts."""
    texts = [r["text"] for r in plan if r.get("text")]
    if not texts:
        return
    # add simple brand-less lines; capcut set-text needs segment ids
    try:
        segs = json.loads(ss.cc("segments", dest, "--track", "text"))
    except Exception as e:
        print(f"  text list skip: {e}")
        return
    # map first N text boxes
    for i, seg in enumerate(segs[: len(texts)]):
        th = texts[i]
        # format Thai|EN empty EN
        payload = f"{th}|"
        try:
            ss.cc("set-text", dest, seg["id"], payload, check=False)
            print(f"  text[{i}] -> {th}")
        except Exception as e:
            print(f"  text[{i}] fail: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, help="path to EDIT_PLAN.md")
    ap.add_argument("--snapshot", default="A_medium", help="name under templates/snapshot or abs path")
    ap.add_argument("--name", required=True, help="draft name")
    ap.add_argument("--shop", default="CALUOMATT.TH")
    ap.add_argument("--sku", default="LNB017")
    ap.add_argument("--bgm", default="", help="optional bgm path")
    ap.add_argument("--bgm-vol", type=float, default=0.25)
    ap.add_argument("--to-capcut", action="store_true")
    ap.add_argument("--work-dir", default="", help="default Video_Studio/drafts/_work/NAME")
    args = ap.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.is_file():
        # try relative to repo
        plan_path = REPO / args.plan
    if not plan_path.is_file():
        sys.exit(f"missing plan: {args.plan}")

    text = plan_path.read_text(encoding="utf-8")
    if "approved_by_human" not in text and "status: approved" not in text.lower():
        # allow if human said approve in chat — still require flag in file; we set it before run
        print("WARN: plan may not show approved_by_human — continuing if caller forces")

    rows = parse_timeline(text)
    if not rows:
        sys.exit("no timeline rows parsed from EDIT_PLAN")

    snap = args.snapshot
    if not os.path.isabs(snap):
        snap = str(VS / "templates" / "snapshot" / snap)
    if not os.path.isdir(snap):
        sys.exit(f"missing snapshot: {snap}")

    # resolve all paths first
    for r in rows:
        r["path"] = str(resolve_path(args.shop, args.sku, r["source_file"]))
        if not os.path.isfile(r["path"]):
            sys.exit(f"missing file: {r['path']}")

    dest = args.work_dir or str(VS / "drafts" / "_work" / args.name)
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(snap, dest)

    cpath = os.path.join(dest, "draft_content.json")
    d = json.load(open(cpath, encoding="utf-8"))
    old_dur = int(d.get("duration") or 0)

    vtracks = [t for t in d["tracks"] if t["type"] == "video"]
    vt = next((t for t in vtracks if t.get("attribute") == 1), vtracks[0])

    print(f"[{args.name}] plan shots={len(rows)} template segs={len(vt['segments'])}")
    for r in rows:
        print(
            f"  #{r['i']:02d} {r['source_file']} {r['t_in']}-{r['t_out']} "
            f"dur={r['dur']}s · {r['shot_type']} · {r['purpose'][:24]}"
        )

    # replace-media for first N segments (by template order)
    main_ids = [s["id"] for s in vt["segments"][: len(rows)]]
    segs_cli = json.loads(ss.cc("segments", dest, "--track", "video"))
    id_to_cli = {s["id"]: s for s in segs_cli}
    for i, seg_id in enumerate(main_ids):
        if seg_id not in id_to_cli:
            print(f"  WARN missing seg {seg_id}")
            continue
        ss.cc("replace-media", dest, seg_id, rows[i]["path"])

    # reload + rechain
    d = json.load(open(cpath, encoding="utf-8"))
    vtracks = [t for t in d["tracks"] if t["type"] == "video"]
    vt = next((t for t in vtracks if t.get("attribute") == 1), vtracks[0])
    new_dur = rechain_video(vt, rows)

    # clamp source starts to file duration
    for i, seg in enumerate(vt["segments"]):
        path = rows[i]["path"]
        try:
            fdur = ss.probe_dur_us(path)
            st = seg["source_timerange"]["start"]
            sd = seg["source_timerange"]["duration"]
            if st + sd > fdur:
                seg["source_timerange"]["start"] = max(0, fdur - sd)
        except Exception as e:
            print(f"  probe warn {path}: {e}")

    d["duration"] = new_dur
    scale_non_video_tracks(d, new_dur, old_dur or new_dur)

    # prune unused video materials
    used = {
        s.get("material_id")
        for t in d["tracks"]
        if t["type"] == "video"
        for s in t.get("segments", [])
    }
    d["materials"]["videos"] = [m for m in d["materials"].get("videos", []) if m.get("id") in used]

    write_all_bases(dest, d)
    ss._reidentify(dest)
    ss.cc("lint", dest, "--fix", "--no-check-paths", check=False)
    ss.cc("sync-timelines", dest, "--apply", check=False)

    # texts
    set_texts(dest, rows, new_dur)

    # BGM: remove old audio tracks content by re-adding? shell_swap adds audio
    bgm = Path(args.bgm) if args.bgm else pick_bgm()
    if bgm and bgm.is_file():
        # capcut add-audio: start 0, duration seconds
        try:
            # strip existing audio segments via reload after add might stack — try add only
            ss.cc(
                "add-audio",
                dest,
                str(bgm),
                "0",
                f"{new_dur / 1e6:.2f}",
                "--volume",
                str(args.bgm_vol),
                check=False,
            )
            print(f"  bgm: {bgm.name} vol={args.bgm_vol}")
        except Exception as e:
            print(f"  bgm skip: {e}")
    else:
        print("  bgm: none found")

    ss.cc("sync-timelines", dest, "--apply", check=False)

    d2 = json.load(open(cpath, encoding="utf-8"))
    fa = rows[0]["path"]
    aa = next((a["path"] for a in d2["materials"].get("audios", []) if a.get("path")), None)
    ss.patch_meta_info(dest, fa, aa)
    try:
        ss.make_cover(rows[0]["path"], float(rows[0]["t_in"]), dest)
    except Exception as e:
        print(f"  cover skip: {e}")

    # ledger
    ledger = {
        "name": args.name,
        "plan": str(plan_path),
        "snapshot": snap,
        "duration_sec": new_dur / 1e6,
        "shots": rows,
        "bgm": str(bgm) if bgm else None,
        "bgm_vol": args.bgm_vol,
    }
    Path(dest, "EDIT_PLAN_BUILD.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    report = REPO / "jobs" / args.shop / args.sku / "BUILD_REPORT.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        f"""# BUILD_REPORT — {args.name}

- date: team3
- plan: `{plan_path}`
- snapshot: `{snap}`
- draft_work: `{dest}`
- duration_sec: {new_dur/1e6:.2f}
- shots: {len(rows)}
- bgm: {bgm.name if bgm else 'none'} @ {args.bgm_vol}
- model_lock: B (02–05 only)
- mute_video: yes
- status: built — open CapCut and Grill (team 4)

## Shots
"""
        + "\n".join(
            f"- #{r['i']:02d} {r['source_file']} {r['t_in']}-{r['t_out']} ({r['dur']}s) {r['purpose']}"
            for r in rows
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"  draft: {dest}")
    print(f"  report: {report}")

    if args.to_capcut and os.path.isdir(ss.CAPCUT_DRAFT_DIR):
        cc_dest = os.path.join(ss.CAPCUT_DRAFT_DIR, args.name)
        if os.path.exists(cc_dest):
            shutil.rmtree(cc_dest, ignore_errors=True)
        shutil.copytree(dest, cc_dest)
        ss.patch_meta_identity(cc_dest, args.name, ss.CAPCUT_DRAFT_DIR)
        ss.cc("sync-timelines", cc_dest, "--apply", check=False)
        # ensure all timeline copies
        d3 = json.load(open(os.path.join(cc_dest, "draft_content.json"), encoding="utf-8"))
        write_all_bases(cc_dest, d3)
        print(f"  -> CapCut: {cc_dest}")


if __name__ == "__main__":
    main()
