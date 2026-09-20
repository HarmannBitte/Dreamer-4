from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from tqdm import tqdm

DEFAULT_STEM = "cheeky-cornflower-setter-02e496ce4abb-20220421-092639"
DEFAULT_VERSION = "10.0"
DEFAULT_INDEX_URL = "https://openaipublic.blob.core.windows.net/minecraft-rl/snapshots/all_10xx_Jun_29.json"


def download(url: str, output_path: Path, *, overwrite: bool) -> None:
    if output_path.exists() and not overwrite:
        print(f"exists: {output_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        with urlopen(url) as response:
            total = int(response.headers.get("Content-Length") or 0)
            with tmp_path.open("wb") as handle:
                with tqdm(
                    total=total or None,
                    unit="B",
                    unit_scale=True,
                    desc=output_path.name,
                ) as progress:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        handle.write(chunk)
                        progress.update(len(chunk))
        shutil.move(str(tmp_path), output_path)
    except URLError as exc:
        if tmp_path.exists():
            tmp_path.unlink()
        raise RuntimeError(f"Failed to download {url}: {exc}") from exc


def resolve_from_index(index_url: str, version: str, stem: str) -> tuple[str, str]:
    with urlopen(index_url) as response:
        index = json.load(response)

    basedir = index.get("basedir")
    relpaths = set(index.get("relpaths", []))
    if not isinstance(basedir, str) or not basedir:
        raise ValueError(f"Index does not contain a valid basedir: {index_url}")

    rel_stem = f"data/{version.strip('/')}/{stem}"
    mp4_relpath = f"{rel_stem}.mp4"
    jsonl_relpath = f"{rel_stem}.jsonl"
    if mp4_relpath not in relpaths:
        raise ValueError(f"VPT index {index_url} does not list the sample video: {mp4_relpath}")

    return f"{basedir.rstrip('/')}/{mp4_relpath}", f"{basedir.rstrip('/')}/{jsonl_relpath}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a small official Minecraft VPT sample MP4 and JSONL actions file.")
    parser.add_argument("--output_dir", type=Path, default=Path("samples/vpt"))
    parser.add_argument("--index_url", default=DEFAULT_INDEX_URL)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--stem", default=DEFAULT_STEM)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mp4_url, jsonl_url = resolve_from_index(args.index_url, args.version, args.stem)
    mp4_path = args.output_dir / f"{args.stem}.mp4"
    jsonl_path = args.output_dir / f"{args.stem}.jsonl"

    print(f"Verified sample video in official VPT index: {args.index_url}")
    download(mp4_url, mp4_path, overwrite=args.overwrite)
    download(jsonl_url, jsonl_path, overwrite=args.overwrite)
    print("Downloaded VPT sample:")
    print(f"  MP4: {mp4_path}")
    print(f"  actions: {jsonl_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise
