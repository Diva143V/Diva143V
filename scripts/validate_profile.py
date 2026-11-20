#!/usr/bin/env python3
"""Validate the generated solar-system profile.

The checks are intentionally narrow: they protect the theme, the facts, and the
things that break when a wide SVG is scaled down on a phone.
"""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
ASSETS = ROOT / "assets"
SVG = "{http://www.w3.org/2000/svg}"

EXPECTED_HEADINGS = content.README_HEADINGS
EXPECTED_IMAGES = 9

# Conservative width factor for a bold system-ui face.
WIDTH = {
    "name-1": {"factor": 0.72, "limit": 420, "min_size": 60},
    "name-2": {"factor": 0.72, "limit": 420, "min_size": 60},
    "name-3": {"factor": 0.72, "limit": 420, "min_size": 60},
    "tagline-1": {"factor": 0.60, "limit": 458, "min_size": 15},
    "tagline-2": {"factor": 0.60, "limit": 458, "min_size": 15},
}

FORBIDDEN = (
    "wasapi",
    "whisper",
    "crates.io",
    "high-assurance",
    "telemetry",
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
    "verified experience",
    "ai-powered",
    "placeholder",
    "lorem ipsum",
)

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)


def _text_width(element: ET.Element, factor: float) -> float:
    value = element.text or ""
    size = float(element.get("font-size", "0"))
    spacing = float(element.get("letter-spacing", "0") or 0)
    return len(value) * size * factor + max(0, len(value) - 1) * spacing


def _is_solar_asset(path: Path) -> bool:
    return path.name.startswith("solar-") or "solar-cards" in path.parts


def validate_svgs() -> list[str]:
    errors: list[str] = []
    svg_files = sorted(ASSETS.rglob("*.svg"))
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
            continue
        if "viewBox" not in root.attrib and not (
            root.get("width") and root.get("height")
        ):
            errors.append(f"{rel}: needs a viewBox or explicit width and height")

        raw = path.read_text(encoding="utf-8")
        if "<script" in raw or "<foreignObject" in raw:
            errors.append(f"{rel}: must not contain script or foreignObject")
        if re.search(r'href="(?!#|data:)', raw):
            errors.append(f"{rel}: must not reference external resources")

        if not _is_solar_asset(path):
            continue

        if root.get("role") != "img":
            errors.append(f'{rel}: must declare role="img"')
        title = root.find(f"{SVG}title")
        desc = root.find(f"{SVG}desc")
        if title is None or not (title.text or "").strip():
            errors.append(f"{rel}: missing a non-empty <title>")
        if desc is None or not (desc.text or "").strip():
            errors.append(f"{rel}: missing a non-empty <desc>")

    return errors


def validate_hero() -> list[str]:
    errors: list[str] = []
    path = ASSETS / "solar-orbits.svg"
    if not path.is_file():
        return ["missing hero: assets/solar-orbits.svg"]

    if path.stat().st_size > 200_000:
        errors.append(f"solar-orbits.svg is {path.stat().st_size} bytes; keep it under 200 KB")

    root = ET.parse(path).getroot()
    if root.get("viewBox") != "0 0 880 520":
        errors.append("solar-orbits.svg viewBox must be 0 0 880 520")

    raw = path.read_text(encoding="utf-8")
    if raw.count("data:image/") != 1:
        errors.append("the hero must embed exactly one avatar image")
    if "@media (prefers-reduced-motion: reduce)" not in raw:
        errors.append("the hero must disable motion for prefers-reduced-motion")
    if ".comet { display: none; }" not in raw:
        errors.append("the comet must be hidden under reduced motion")

    title = root.find(f"{SVG}title")
    desc = root.find(f"{SVG}desc")
    if title is None or (title.text or "").strip() != content.HERO_ALT:
        errors.append("hero <title> must match content.HERO_ALT")
    if desc is None or (desc.text or "").strip() != content.HERO_DESC:
        errors.append("hero <desc> must match content.HERO_DESC")

    for element_id, rule in WIDTH.items():
        element = root.find(f".//{SVG}text[@id='{element_id}']")
        if element is None:
            errors.append(f"hero is missing text id={element_id}")
            continue
        value = (element.text or "").strip()
        if not value:
            errors.append(f"hero text id={element_id} is empty")
            continue
        size = float(element.get("font-size", "0"))
        x = float(element.get("x", "0"))
        if size < rule["min_size"]:
            errors.append(f"hero text id={element_id} is below {rule['min_size']}px")
        right = x + _text_width(element, rule["factor"])
        if right > rule["limit"]:
            errors.append(
                f"hero text id={element_id} may reach x={right:.0f}; "
                f"limit is {rule['limit']}"
            )

    return errors


def validate_layout_assets() -> list[str]:
    errors: list[str] = []
    expected = {
        "solar-about.svg": "0 0 880 214",
        "solar-stack.svg": "0 0 880 226",
        "solar-log.svg": "0 0 880 148",
        "solar-footer.svg": "0 0 880 86",
    }
    for name, view_box in expected.items():
        path = ASSETS / name
        if not path.is_file():
            errors.append(f"missing asset: {name}")
            continue
        root = ET.parse(path).getroot()
        if root.get("viewBox") != view_box:
            errors.append(f"{name} viewBox must be {view_box}")

    for project in content.PROJECTS:
        path = ASSETS / "solar-cards" / f"card-{project.name.lower()}.svg"
        if not path.is_file():
            errors.append(f"missing card: {path.relative_to(ROOT)}")
            continue
        root = ET.parse(path).getroot()
        if root.get("viewBox") != "0 0 430 168":
            errors.append(f"{path.name} viewBox must be 0 0 430 168")
        raw = path.read_text(encoding="utf-8")
        if "data:image/" in raw:
            errors.append(f"{path.name} should not embed the avatar")

    return errors


def validate_readme() -> list[str]:
    errors: list[str] = []
    if not README_PATH.is_file():
        return ["README.md does not exist"]

    raw = README_PATH.read_text(encoding="utf-8")
    lines = raw.splitlines()

    if not raw.startswith("<!-- Generated by scripts/generate_solar.py."):
        errors.append("README.md is missing its generated-file notice")

    for phrase in FORBIDDEN:
        if phrase in raw.lower():
            errors.append(f"README.md contains an unsupported claim or stock phrase: {phrase!r}")

    if EMOJI_RE.search(raw):
        errors.append("README.md contains emoji")
    if "img.shields.io" in raw:
        errors.append("README.md contains a badge wall")
    plain = re.sub(r"<[^>]+>", "", raw)
    if re.search(r"\b\d+%", plain):
        errors.append("README.md contains an unverified percentage")

    headings = [line[3:].strip() for line in lines if line.startswith("## ")]
    if tuple(headings) != EXPECTED_HEADINGS:
        errors.append(f"README.md headings must be {EXPECTED_HEADINGS}, got {tuple(headings)}")
    if any(line.startswith("# ") for line in lines):
        errors.append("README.md must not use an H1; the hero is the title")

    images = re.findall(r"<img\b[^>]*>", raw)
    if len(images) != EXPECTED_IMAGES:
        errors.append(f"README.md should use {EXPECTED_IMAGES} images, found {len(images)}")
    for image in images:
        src_match = re.search(r'src="([^"]+)"', image)
        alt_match = re.search(r'alt="([^"]*)"', image)
        if not src_match or not alt_match:
            errors.append("every image needs a src and alt text")
            continue
        src, alt = src_match.group(1), html.unescape(alt_match.group(1))
        if not alt.strip():
            errors.append(f"image {src} has empty alt text")
        if src.startswith(("http://", "https://")):
            errors.append(f"image {src} must be local")
        else:
            local = ROOT / src
            if not local.is_file():
                errors.append(f"missing local image: {src}")
            elif local.stat().st_size == 0:
                errors.append(f"empty local image: {src}")

    if sum('width="100%"' in image for image in images) != EXPECTED_IMAGES:
        errors.append("every image should be set to width=\"100%\"")

    for project in content.PROJECTS:
        if f"href=\"{project.url}\"" not in raw:
            errors.append(f"README.md is missing the link for {project.name}")
        if f"card-{project.name.lower()}.svg" not in raw:
            errors.append(f"README.md is missing the card for {project.name}")

    if content.SMALLER not in raw:
        errors.append("README.md is missing the smaller-projects line")
    if "Windows Live Captions" not in raw:
        errors.append("README.md should state that LiveSubs reads Windows Live Captions")

    allowed_repos = content.all_repo_urls()
    link_urls = re.findall(r'\]\(([^)\s]+)\)', raw) + re.findall(
        r'href="([^"]+)"', raw
    )
    for url in link_urls:
        if not re.match(r"^(https://|mailto:)", url):
            errors.append(f"README.md has an insecure or relative link: {url}")
        if url.startswith("https://github.com/"):
            owner_repo = "/".join(url.split("/")[:5])
            if owner_repo not in allowed_repos:
                errors.append(f"README.md links to an unlisted repository: {url}")

    for token in ("http://", "file://", "javascript:"):
        if token in raw:
            errors.append(f"README.md contains a forbidden link scheme: {token}")

    if any(line != line.rstrip() for line in lines):
        errors.append("README.md has trailing whitespace")
    if raw.count("\n\n\n") > 0:
        errors.append("README.md has more than one blank line in a row")

    words = len(re.findall(r"[A-Za-z0-9']+", raw))
    if not 350 <= words <= 850:
        errors.append(f"README.md is {words} words; keep it between 350 and 850")

    return errors


def main() -> int:
    print("[validate] svg files")
    svg_errors = validate_svgs()
    print("[validate] hero")
    hero_errors = validate_hero()
    print("[validate] layout")
    layout_errors = validate_layout_assets()
    print("[validate] readme")
    readme_errors = validate_readme()

    errors = svg_errors + hero_errors + layout_errors + readme_errors
    if errors:
        print(f"\n[validate] FAILED ({len(errors)} issue(s)):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("\n[validate] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
