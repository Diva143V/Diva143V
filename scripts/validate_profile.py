#!/usr/bin/env python3
"""
NEBULA / 01 — Profile Integrity & Anti-Slop Validator
Author: Diva143V
Description: Validates SVG XML syntax, local image references, link formats, and anti-slop rules.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
README_PATH = os.path.join(ROOT_DIR, "README.md")


def validate_svg_files():
    """Verify all SVG files parse as valid XML and have necessary dimensions."""
    print("[Validator] Checking SVG files...")
    errors = []
    svg_files = []
    
    for root, _, files in os.walk(ASSETS_DIR):
        for f in files:
            if f.endswith(".svg"):
                svg_files.append(os.path.join(root, f))
                
    if not svg_files:
        errors.append("No SVG files found in assets directory!")
        
    for p in svg_files:
        rel_path = os.path.relpath(p, ROOT_DIR)
        try:
            tree = ET.parse(p)
            root_el = tree.getroot()
            if not root_el.tag.endswith("svg"):
                errors.append(f"{rel_path}: Root tag is not <svg> (got {root_el.tag})")
            if "viewBox" not in root_el.attrib and ("width" not in root_el.attrib or "height" not in root_el.attrib):
                errors.append(f"{rel_path}: Missing viewBox or width/height attributes")
        except ET.ParseError as e:
            errors.append(f"{rel_path}: XML parse error: {e}")
        except Exception as e:
            errors.append(f"{rel_path}: Unexpected error: {e}")
            
    print(f"[Validator] Checked {len(svg_files)} SVG files.")
    return errors


def validate_readme():
    """Verify README links, images, and ensure no forbidden slop tokens exist."""
    print("[Validator] Checking README.md...")
    errors = []
    
    if not os.path.isfile(README_PATH):
        return ["README.md does not exist!"]
        
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check for placeholder/slop tokens
    forbidden_tokens = ["TODO", "FIXME", "lorem ipsum", "undefined", "[X]", "YOUR_NAME", "PLACEHOLDER"]
    for token in forbidden_tokens:
        if token.lower() in content.lower():
            errors.append(f"Forbidden placeholder token found in README: '{token}'")
            
    # Check local image references in markdown and HTML
    img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    md_img_matches = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
    all_images = img_matches + md_img_matches
    
    checked_local_imgs = 0
    for img in all_images:
        if not img.startswith("http://") and not img.startswith("https://"):
            checked_local_imgs += 1
            local_path = os.path.join(ROOT_DIR, img.replace("/", os.sep))
            if not os.path.isfile(local_path):
                errors.append(f"Referenced image file does not exist: {img}")
            elif os.path.getsize(local_path) == 0:
                errors.append(f"Referenced image file is empty: {img}")
                
    print(f"[Validator] Checked {checked_local_imgs} local image references in README.")
    
    # Check project links
    links = re.findall(r'href=["\']([^"\']+)["\']', content)
    md_links = re.findall(r'\[.*?\]\((https?://[^)]+)\)', content)
    all_links = links + md_links
    
    for l in all_links:
        if l.startswith("https://github.com/Diva143V/"):
            repo_name = l.split("https://github.com/Diva143V/")[1].split("/")[0].split("#")[0]
            # Known verified repositories
            verified_repos = [
                "LiveSubs", "Griffin", "SyGriffin", "Knox", "Kg-Library-API", 
                "chatstream", "myselfdiva", "Laya-KG", "vinu", "forage-midas", "Diva143V"
            ]
            if repo_name and repo_name not in verified_repos:
                errors.append(f"Link points to unverified repository: {l}")
                
    return errors


def main():
    print("[Validator] Starting NEBULA / 01 Validation Suite...")
    svg_errors = validate_svg_files()
    readme_errors = validate_readme()
    
    all_errors = svg_errors + readme_errors
    if all_errors:
        print("\n[Validator] ❌ FAILED with errors:")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
        
    print("\n[Validator] ✅ All validation checks PASSED perfectly!")
    sys.exit(0)


if __name__ == "__main__":
    main()
