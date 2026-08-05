#!/usr/bin/env python3
"""Validate and build cross-platform HDF Blog Editor release archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import py_compile
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "hdf-blog-editor"
DIST = ROOT / "dist"
FIXTURES = ROOT / "tests" / "fixtures"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
RELEASE_DATE = (ROOT / "RELEASE_DATE").read_text(encoding="utf-8").strip()
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


class ReleaseError(RuntimeError):
    pass


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ReleaseError(f"Missing YAML frontmatter: {path}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            raise ReleaseError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def check_skill() -> None:
    required = [
        SKILL / "SKILL.md",
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "house-style.md",
        SKILL / "references" / "wordpress-retrofit.md",
        SKILL / "references" / "output-contract.md",
        SKILL / "scripts" / "check_markup.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise ReleaseError(f"Missing required files: {', '.join(missing)}")

    frontmatter = read_frontmatter(SKILL / "SKILL.md")
    if set(frontmatter) != {"name", "description"}:
        raise ReleaseError("SKILL.md frontmatter must contain only name and description")
    if frontmatter["name"] != SKILL.name:
        raise ReleaseError("Skill folder name must match frontmatter name")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", frontmatter["name"]):
        raise ReleaseError("Invalid skill name")
    if len(frontmatter["description"]) > 200:
        raise ReleaseError("Description exceeds Claude's 200-character limit")

    skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(SKILL.rglob("*"))
        if path.is_file()
    )
    lower = skill_text.lower()
    for forbidden in ("/users/", "todo", "excerpt"):
        if forbidden in lower:
            raise ReleaseError(f"Forbidden source text found in canonical skill: {forbidden}")

    if len((SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()) >= 500:
        raise ReleaseError("SKILL.md must remain under 500 lines")

    output_contract = (SKILL / "references" / "output-contract.md").read_text(encoding="utf-8")
    for phrase in ("Reader preview", "WordPress HTML", "Exact inline-image placement", "Pre-delivery gate"):
        if phrase not in output_contract:
            raise ReleaseError(f"Output contract is missing: {phrase}")

    py_compile.compile(str(SKILL / "scripts" / "check_markup.py"), doraise=True)

    for document in (ROOT / "README.md", ROOT / "INSTALL.md"):
        if VERSION not in document.read_text(encoding="utf-8"):
            raise ReleaseError(f"{document.name} does not mention current version {VERSION}")


def check_markup_fixtures() -> None:
    checker = SKILL / "scripts" / "check_markup.py"
    cases = (("clean.html", 0), ("contaminated.html", 1))
    for filename, expected in cases:
        result = subprocess.run(
            [sys.executable, str(checker), str(FIXTURES / filename)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != expected:
            raise ReleaseError(
                f"Markup fixture {filename} returned {result.returncode}, expected {expected}\n{result.stdout}{result.stderr}"
            )


def check_evals() -> None:
    eval_path = ROOT / "tests" / "evals.json"
    try:
        cases = json.loads(eval_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReleaseError(f"Invalid evaluation file: {error}") from error
    if not isinstance(cases, list) or len(cases) < 6:
        raise ReleaseError("At least six cross-platform evaluation cases are required")
    names: set[str] = set()
    for case in cases:
        if not isinstance(case, dict) or not {"name", "prompt", "must"} <= set(case):
            raise ReleaseError("Every evaluation needs name, prompt and must fields")
        if case["name"] in names:
            raise ReleaseError(f"Duplicate evaluation name: {case['name']}")
        names.add(case["name"])
        if not isinstance(case["must"], list) or not case["must"]:
            raise ReleaseError(f"Evaluation has no assertions: {case['name']}")


def iter_files(source: Path, exclude: set[str] | None = None):
    excluded = exclude or set()
    for path in sorted(source.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(source)
        if relative.parts and relative.parts[0] in excluded:
            continue
        yield path, relative


def write_entry(archive: zipfile.ZipFile, source: Path, destination: str) -> None:
    info = zipfile.ZipInfo(destination, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o755 if source.suffix == ".py" else 0o644) << 16
    archive.writestr(info, source.read_bytes())


def build_chatgpt(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for source, relative in iter_files(SKILL):
            write_entry(archive, source, str(Path("hdf-blog-editor") / relative))


def build_claude(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for source, relative in iter_files(SKILL, exclude={"agents"}):
            write_entry(archive, source, str(Path("hdf-blog-editor") / relative))


def build_antigravity(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        prefix = Path(".agent") / "skills" / "hdf-blog-editor"
        for source, relative in iter_files(SKILL, exclude={"agents"}):
            write_entry(archive, source, str(prefix / relative))
        workflow = ROOT / "adapters" / "antigravity" / "review-hdf-blog.md"
        install = ROOT / "adapters" / "antigravity" / "INSTALL-ANTIGRAVITY.md"
        write_entry(archive, workflow, ".agents/workflows/review-hdf-blog.md")
        write_entry(archive, install, "INSTALL-ANTIGRAVITY.md")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive(path: Path, platform: str) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ReleaseError(f"Duplicate entries in {path.name}")
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ReleaseError(f"Unsafe path in {path.name}")
        if platform in {"chatgpt", "claude"}:
            required = "hdf-blog-editor/SKILL.md"
        else:
            required = ".agent/skills/hdf-blog-editor/SKILL.md"
        if required not in names:
            raise ReleaseError(f"Missing {required} in {path.name}")


def build() -> list[Path]:
    if DIST.exists():
        for old in DIST.glob("*.zip"):
            old.unlink()
        for old_name in ("SHA256SUMS", "release-manifest.json"):
            old = DIST / old_name
            if old.exists():
                old.unlink()
    else:
        DIST.mkdir(parents=True)

    archives = {
        "chatgpt": DIST / f"hdf-blog-editor-chatgpt-v{VERSION}.zip",
        "claude": DIST / f"hdf-blog-editor-claude-v{VERSION}.zip",
        "antigravity": DIST / f"hdf-blog-editor-antigravity-v{VERSION}.zip",
    }
    build_chatgpt(archives["chatgpt"])
    build_claude(archives["claude"])
    build_antigravity(archives["antigravity"])

    for platform, path in archives.items():
        validate_archive(path, platform)

    artifacts = {
        platform: {"file": path.name, "sha256": sha256(path), "bytes": path.stat().st_size}
        for platform, path in archives.items()
    }
    manifest = {
        "name": "hdf-blog-editor",
        "version": VERSION,
        "release_date": RELEASE_DATE,
        "artifacts": artifacts,
    }
    (DIST / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sums = "\n".join(f"{artifacts[p]['sha256']}  {artifacts[p]['file']}" for p in sorted(artifacts))
    (DIST / "SHA256SUMS").write_text(sums + "\n", encoding="utf-8")
    return list(archives.values())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "build", "all"))
    args = parser.parse_args()

    check_skill()
    check_markup_fixtures()
    check_evals()
    print("Canonical skill, fixtures and evaluation definitions passed.")

    if args.command in {"build", "all"}:
        archives = build()
        for path in archives:
            print(f"Built {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
