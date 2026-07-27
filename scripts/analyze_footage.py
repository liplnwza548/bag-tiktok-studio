# -*- coding: utf-8 -*-
"""
Team 1 — Footage Analyzer
Usage:
  python scripts/analyze_footage.py --sku-dir PATH --shop CALUOMATT.TH --sku LNB017
  python scripts/analyze_footage.py --sku-dir PATH --out FOOTAGE.md

Reads GEMINI_API_KEY from env, or Google Gemini API Key from vault SECRET.md
Creates lightweight proxies (no audio) then calls Gemini with prompts/footage_analyzer.md
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROMPT_PATH = REPO / "prompts" / "footage_analyzer.md"
SCHEMA_PATH = REPO / "docs" / "schemas" / "FOOTAGE.schema.md"
FFMPEG = r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe"
if not Path(FFMPEG).exists():
    FFMPEG = "ffmpeg"

VIDEO_EXT = {".mov", ".mp4", ".m4v", ".mkv"}


def load_api_key() -> str:
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k:
        return k.strip()
    secret = Path(r"C:\Users\Administrator\Documents\Obsidian Vault\SECRET.md")
    if secret.exists():
        text = secret.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"Google Gemini API Key\s*:\s*\n?\s*(\S+)", text)
        if m:
            return m.group(1).strip()
    raise SystemExit("No GEMINI_API_KEY / SECRET.md Gemini key found")


def find_videos(sku_dir: Path) -> list[Path]:
    vids = []
    for p in sorted(sku_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in VIDEO_EXT:
            # skip proxies
            if "proxy" in p.parts or p.name.startswith("_proxy_"):
                continue
            vids.append(p)
    return vids


def make_proxy(src: Path, proxy_dir: Path) -> Path:
    proxy_dir.mkdir(parents=True, exist_ok=True)
    out = proxy_dir / f"_proxy_{src.stem}.mp4"
    if out.exists() and out.stat().st_size > 10_000:
        return out
    # low-res, low-fps, no audio — enough for shot labeling
    cmd = [
        FFMPEG,
        "-y",
        "-i",
        str(src),
        "-vf",
        "scale=540:-2,fps=2",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-an",
        "-movflags",
        "+faststart",
        str(out),
    ]
    print(f"  proxy {src.name} -> {out.name} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not out.exists():
        print(r.stderr[-2000:] if r.stderr else "ffmpeg failed", file=sys.stderr)
        raise SystemExit(f"ffmpeg failed for {src}")
    print(f"  ok {out.stat().st_size // 1024} KB", flush=True)
    return out


def wait_file_active(genai, f, timeout=600):
    start = time.time()
    while getattr(f, "state", None) and f.state.name == "PROCESSING":
        if time.time() - start > timeout:
            raise TimeoutError(f"file processing timeout: {f.name}")
        time.sleep(3)
        f = genai.get_file(f.name)
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sku-dir", required=True, help="Folder with raw videos (or subfolders)")
    ap.add_argument("--shop", default="UNKNOWN")
    ap.add_argument("--sku", default="")
    ap.add_argument("--out", default="", help="Output FOOTAGE.md path")
    ap.add_argument("--model", default="models/gemini-2.5-flash")
    ap.add_argument("--max-files", type=int, default=0, help="0 = all")
    ap.add_argument("--skip-proxy", action="store_true", help="Upload originals (slow/large)")
    args = ap.parse_args()

    sku_dir = Path(args.sku_dir)
    if not sku_dir.is_dir():
        raise SystemExit(f"not a dir: {sku_dir}")

    sku = args.sku or sku_dir.name
    shop = args.shop
    out = Path(args.out) if args.out else (REPO / "jobs" / shop / sku / "FOOTAGE.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    proxy_dir = out.parent / "_proxies"

    vids = find_videos(sku_dir)
    if not vids:
        raise SystemExit(f"no videos under {sku_dir}")
    if args.max_files:
        vids = vids[: args.max_files]
    print(f"found {len(vids)} videos", flush=True)

    import google.generativeai as genai

    genai.configure(api_key=load_api_key())
    model = genai.GenerativeModel(args.model)

    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    system = (
        f"{prompt}\n\n---\n# SCHEMA TO FOLLOW\n{schema}\n\n"
        f"sku={sku} shop={shop}\n"
        "Fill FOOTAGE.md for ALL attached clips. "
        "Use real filenames (without _proxy_ prefix if proxy). "
        "Timestamps in seconds of the ORIGINAL clip timeline (proxy is same length, 2fps).\n"
        "Respond with ONLY the markdown FOOTAGE.md body.\n"
    )

    # Note: some Gemini keys (AQ.*) accept generateContent + inline video
    # but reject File API upload (API_KEY_INVALID). Prefer inline bytes.
    parts: list = [system]
    attached = []
    for src in vids:
        try:
            media = src if args.skip_proxy else make_proxy(src, proxy_dir)
            size_mb = media.stat().st_size / (1024 * 1024)
            print(f"  attach inline {src.name} via {media.name} ({size_mb:.1f} MB)...", flush=True)
            if size_mb > 18:
                print(f"  WARN skip {src.name}: proxy too large for inline (>18MB)", flush=True)
                continue
            data = media.read_bytes()
            parts.append(f"\n### FILE: {src.name}\n")
            parts.append({"mime_type": "video/mp4", "data": data})
            attached.append(src.name)
        except Exception as e:
            print(f"  WARN skip {src.name}: {e}", flush=True)

    if not attached:
        raise SystemExit("no files attached")

    print(f"generate with {args.model} ({len(attached)} files)...", flush=True)
    resp = model.generate_content(
        parts,
        generation_config={"temperature": 0.2, "max_output_tokens": 8192},
        request_options={"timeout": 600},
    )
    text = (resp.text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:markdown|md)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    # ensure frontmatter has sku/shop if missing
    if not text.lstrip().startswith("---"):
        header = (
            f"---\nsku: {sku}\nshop: {shop}\nanalyzer: gemini-2.5-flash\n"
            f"files_count: {len(attached)}\ndate: {time.strftime('%Y-%m-%d')}\n"
            f"method: inline_video_proxy\n---\n\n"
        )
        text = header + text

    out.write_text(text + "\n", encoding="utf-8")
    print(f"WROTE {out}", flush=True)
    print("files:", ", ".join(attached), flush=True)


if __name__ == "__main__":
    main()
