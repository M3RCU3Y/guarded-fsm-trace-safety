from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_SUFFIXES = {".tex", ".bib", ".pdf", ".docx", ".aux", ".bbl", ".blg", ".log", ".out", ".pyc"}
FORBIDDEN_DIRS = {"submission", "archive", "tmp", "__pycache__"}
IGNORED_DIRS = {".git"}
FORBIDDEN_TEXT_PARTS = [
    ("Chat", "GPT"),
    ("Open", "AI"),
    ("Co", "dex"),
    ("AI", "-", "generated"),
    ("generated", " by ", "AI"),
    ("paper", " source"),
    ("manuscript", " source"),
]


def main() -> None:
    problems: list[str] = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if any(part in FORBIDDEN_DIRS for part in rel.parts):
            problems.append(f"forbidden directory entry: {rel.as_posix()}")
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"forbidden file type: {rel.as_posix()}")
        if path.name == "check_release.py":
            continue
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".json", ".yml", ".yaml", ".cff", ".svg", ".csv"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle in ("".join(parts) for parts in FORBIDDEN_TEXT_PARTS):
                if needle in text:
                    problems.append(f"blocked text pattern in: {rel.as_posix()}")

    if problems:
        raise SystemExit("\n".join(problems))
    print("Release folder check passed.")


if __name__ == "__main__":
    main()
