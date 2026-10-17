#!/usr/bin/env python3
"""Validate repository structure and the skill's non-negotiable workflow."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "novel-to-manhua"
MARKDOWN = [ROOT / "README.md", SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]
errors = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


for page in MARKDOWN:
    check(page.is_file(), f"Missing Markdown file: {page.relative_to(ROOT)}")
    if not page.is_file():
        continue
    content = page.read_text(encoding="utf-8")
    for raw_link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
        parsed = urlsplit(raw_link)
        if parsed.scheme or not parsed.path:
            continue
        target = (page.parent / unquote(parsed.path)).resolve()
        check(target.is_relative_to(ROOT) and target.exists(), f"Broken link in {page.relative_to(ROOT)}: {raw_link}")

skill_file = SKILL / "SKILL.md"
if skill_file.is_file():
    content = skill_file.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    check(frontmatter is not None, "SKILL.md needs YAML frontmatter")
    if frontmatter:
        fields = dict(re.findall(r"^([a-z-]+):\s*(.*)$", frontmatter.group(1), re.MULTILINE))
        check(fields.get("name") == SKILL.name, "Skill name must match its directory")
        description = fields.get("description", "")
        check(bool(description) and len(description) <= 1024, "Skill description must contain 1–1024 characters")
    draw = content.find("**先生成无字画面。**")
    letter = content.find("**后配文字。**")
    deliver = content.find("**向作者交付成品。**")
    check(draw >= 0 and letter > draw, "Workflow must draw text-free art before lettering")
    check(deliver > letter and "不放进作者最终版本" in content, "Author delivery must follow lettering and exclude internal art")
    check("至少 30 页正文" in content and "封面另计" in content, "Default complete script needs at least 30 story pages, excluding the cover")
    check("火柴人" in content and "黑圆点" in content, "Reference style anchors are missing")

assets = list((SKILL / "assets").glob("*.jpg"))
check(bool(assets), "No reference JPG assets found")

eval_file = ROOT / "novel-to-manhua-workspace" / "evals" / "evals.json"
try:
    data = json.loads(eval_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top-level value must be an object")
    evals = data["evals"]
    check(data.get("skill_name") == SKILL.name, "Eval skill_name does not match")
    if not isinstance(evals, list) or not evals:
        raise ValueError("evals must be a non-empty list")
    if any(not isinstance(case, dict) for case in evals):
        raise ValueError("each eval must be an object")
    ids = [case.get("id") for case in evals]
    if any(not isinstance(case_id, int) or case_id <= 0 for case_id in ids):
        raise ValueError("eval IDs must be positive integers")
    check(len(ids) == len(set(ids)), "Eval IDs must be unique")
    for case in evals:
        check(bool(case.get("prompt")) and bool(case.get("expected_output")), f"Eval {case.get('id')} is incomplete")
except (OSError, ValueError, KeyError, TypeError) as exc:
    errors.append(f"Invalid evals.json: {exc}")
    evals = []

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Validated {len(MARKDOWN)} Markdown files, {len(assets)} JPG assets, {len(evals)} evals")
