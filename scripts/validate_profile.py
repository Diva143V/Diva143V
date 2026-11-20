#!/usr/bin/env python3
"""Checks the generated profile for the failures that are easy to miss.

This is deliberately opinionated. It catches the things that made the old
profile look machine-written and the things that break when an SVG is scaled
down on a phone:

* text that runs outside its box, using a conservative width bound
* tiny type inside the hero
* missing accessible names, embedded fonts, or reduced-motion handling
* dead links, unknown repositories, leftover placeholder copy
* a badge wall, emoji headings, or stock AI marketing language
"""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
HERO_PATH = ROOT / "assets" / "hero.svg"
FONT_DIR = ROOT / "assets" / "fonts"

SVG = "{http://www.w3.org/2000/svg}"

# Conservative glyph widths. The real Archivo subset is narrower than this,
# so anything that passes here has room to spare.
WIDTH_FACTOR = {"display": 0.74, "mono": 0.62}

LAYOUT = {
    "name-1": {"max_right": 550, "min_size": 80, "width_class": "display"},
    "name-2": {"max_right": 550, "min_size": 80, "width_class": "display"},
    "name-3": {"max_right": 550, "min_size": 80, "width_class": "display"},
    "caption-1": {"max_right": 770, "min_size": 22, "width_class": "mono"},
    "caption-2": {"max_right": 770, "min_size": 22, "width_class": "mono"},
}

FORBIDDEN_PHRASES = (
    "passionate",
    "leverage",
    "cutting-edge",
    "cutting edge",
    "seamless",
    "game-changer",
    "game changer",
    "unleash",
    "delve",
    "elevate",
    "bespoke",
    "high-assurance",
    "state-of-the-art",
    "state of the art",
    "at the intersection",
    "journey",
    "synergy",
    "empower",
    "revolutionize",
    "world-class",
    "rockstar",
    "ninja",
    "guru",
    "telemetry",
    "orbit",
    "nebula",
    "solar system",
    "transmission channel",
    "moons",
    "planets",
    "verified experience",
    "resume padding",
    "résumé padding",
    "anti-slop",
    "placeholder",
)

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)

EXPECTED_HEADINGS = ("What I'm building", "Where I've worked", "Elsewhere")


def _text_width(element: ET.Element, factor: float) -> float:
    value = element.text or ""
    size = float(element.get("font-size", "0"))
    spacing = float(element.get("letter-spacing", "0") or 0)
    return len(value) * size * factor + max(0, len(value) - 1) * spacing


def _validate_svg_files() -> list[str]:
    """Basic checks for every SVG under assets/, not just the hero."""
    errors: list[str] = []
    svg_files = sorted((ROOT / "assets").rglob("*.svg"))
    if not svg_files:
        return ["no SVG files found under assets/"]

    for path in svg_files:
        rel = path.relative_to(ROOT)
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            errors.append(f"{rel}: invalid XML ({exc})")
            continue

        if root.tag != f"{SVG}svg":
            errors.append(f"{rel}: root element is not <svg>")
        if "viewBox" not in root.attrib and not (
            root.get("width") and root.get("height")
        ):
            errors.append(f"{rel}: needs a viewBox or explicit width and height")
        if "<script" in path.read_text(encoding="utf-8"):
            errors.append(f"{rel}: must not contain script")

    return errors


def validate_hero() -> list[str]:
    errors: list[str] = []

    if not HERO_PATH.is_file():
        return [f"missing hero: {HERO_PATH.relative_to(ROOT)}"]

    size = HERO_PATH.stat().st_size
    if size > 200_000:
        errors.append(f"hero.svg is {size} bytes; keep it under 200 KB")

    try:
        root = ET.parse(HERO_PATH).getroot()
    except ET.ParseError as exc:
        return [f"hero.svg is not valid XML: {exc}"]

    if root.tag != f"{SVG}svg":
        errors.append("hero.svg root element is not <svg>")
        return errors

    if root.get("viewBox") != "0 0 880 480":
        errors.append("hero.svg viewBox must be 0 0 880 480")
    if root.get("role") != "img":
        errors.append('hero.svg must declare role="img"')

    title = root.find(f"{SVG}title")
    desc = root.find(f"{SVG}desc")
    if title is None or (title.text or "").strip() != content.HERO_ALT:
        errors.append("hero.svg <title> must match content.HERO_ALT")
    if desc is None or (desc.text or "").strip() != content.HERO_DESC:
        errors.append("hero.svg <desc> must match content.HERO_DESC")

    raw = HERO_PATH.read_text(encoding="utf-8")
    if raw.count("data:font/woff2;base64,") != 2:
        errors.append("hero.svg must embed exactly the two WOFF2 subsets")
    if "@media (prefers-reduced-motion: reduce)" not in raw:
        errors.append("hero.svg must disable motion for prefers-reduced-motion")
    if ".playhead { display: none; }" not in raw:
        errors.append("the playhead must be hidden under reduced motion")
    if "<script" in raw or "<foreignObject" in raw:
        errors.append("hero.svg must not contain script or foreignObject")
    if re.search(r'href="(?!data:)', raw):
        errors.append("hero.svg must not reference external resources")

    for element_id, rule in LAYOUT.items():
        element = root.find(f".//{SVG}text[@id='{element_id}']")
        if element is None:
            errors.append(f"hero.svg is missing text id={element_id}")
            continue

        text = (element.text or "").strip()
        if not text:
            errors.append(f"text id={element_id} is empty")
            continue

        font_size = float(element.get("font-size", "0"))
        if font_size < rule["min_size"]:
            errors.append(
                f"text id={element_id} is {font_size}px; "
                f"minimum is {rule['min_size']}px"
            )

        x = float(element.get("x", "0"))
        right = x + _text_width(element, WIDTH_FACTOR[rule["width_class"]])
        if x < 40:
            errors.append(f"text id={element_id} starts at x={x}; safe margin is 40")
        if right > rule["max_right"]:
            errors.append(
                f"text id={element_id} may reach x={right:.0f}; "
                f"limit is {rule['max_right']}"
            )

    for name in ("archivo-800.woff2", "dmmono-400.woff2"):
        path = FONT_DIR / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing embedded font source: {name}")

    for name in ("OFL-Archivo.txt", "OFL-DMMono.txt"):
        if not (FONT_DIR / name).is_file():
            errors.append(f"missing font license: {name}")

    return errors


def validate_readme() -> list[str]:
    errors: list[str] = []

    if not README_PATH.is_file():
        return ["README.md does not exist"]

    raw = README_PATH.read_text(encoding="utf-8")
    lines = raw.splitlines()

    if not raw.startswith("<!-- Generated by scripts/build_profile.py."):
        errors.append("README.md is missing its generated-file notice")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in raw.lower():
            errors.append(f"README.md contains stock language: {phrase!r}")

    if EMOJI_RE.search(raw):
        errors.append("README.md contains emoji")

    if "img.shields.io" in raw:
        errors.append("README.md contains a badge wall")

    headings = [line[3:].strip() for line in lines if line.startswith("## ")]
    if tuple(headings) != EXPECTED_HEADINGS:
        errors.append(f"README.md headings must be {EXPECTED_HEADINGS}, got {tuple(headings)}")

    if any(line.startswith("# ") for line in lines):
        errors.append("README.md must not use an H1; the hero is the title")

    if len(re.findall(r"<img\b", raw)) != 1:
        errors.append("README.md should use exactly one image (the hero)")

    hero_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', raw)
    if not hero_match:
        errors.append("README.md is missing the hero image with alt text")
    else:
        src, alt = hero_match.groups()
        if src != "assets/hero.svg":
            errors.append(f"README.md hero src is {src!r}")
        if html.unescape(alt) != content.HERO_ALT:
            errors.append("README.md hero alt does not match content.HERO_ALT")

    for src in re.findall(r'<img[^>]+src="([^"]+)"', raw):
        if not src.startswith(("http://", "https://")):
            if not (ROOT / src).is_file():
                errors.append(f"README.md references a missing local image: {src}")

    if "width=\"100%\"" not in raw:
        errors.append("the hero must be set to width=\"100%\"")

    for project in content.PROJECTS:
        needle = f"**[{project.name}]({project.url})**"
        count = raw.count(needle)
        if count != 1:
            errors.append(
                f"project {project.name} must appear exactly once as {needle!r} "
                f"(found {count})"
            )

    if content.SMALLER not in raw:
        errors.append("README.md is missing the 'smaller things' line")

    # Links: every GitHub repo link must be one we deliberately chose.
    allowed_repos = content.all_repo_urls()
    for url in re.findall(r"\((https?://[^)\s]+)\)", raw):
        if url.startswith("https://github.com/"):
            owner_repo = "/".join(url.split("/")[:5])
            if owner_repo not in allowed_repos:
                errors.append(f"README.md links to an unlisted repository: {url}")

    for url in re.findall(r"\]\(([^)\s]+)\)", raw):
        if not re.match(r"^(https://|mailto:)", url):
            errors.append(f"README.md has an insecure or relative link: {url}")

    forbidden_links = ("http://", "file://", "javascript:")
    for token in forbidden_links:
        if token in raw:
            errors.append(f"README.md contains a forbidden link scheme: {token}")

    if any(line != line.rstrip() for line in lines):
        errors.append("README.md has trailing whitespace")

    words = len(re.findall(r"[A-Za-z0-9']+", raw))
    if not 250 <= words <= 700:
        errors.append(f"README.md is {words} words; keep it between 250 and 700")

    if raw.count("\n\n\n") > 0:
        errors.append("README.md has more than one blank line in a row")

    return errors


def main() -> int:
    print("[validate] svg files")
    svg_errors = _validate_svg_files()
    print("[validate] hero")
    hero_errors = validate_hero()
    print("[validate] readme")
    readme_errors = validate_readme()

    errors = svg_errors + hero_errors + readme_errors
    if errors:
        print(f"\n[validate] FAILED ({len(errors)} issue(s)):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("\n[validate] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
