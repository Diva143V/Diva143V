#!/usr/bin/env python3
"""
NEBULA / 01 — Profile Asset & README Generator
Author: Diva143V
Description: Deterministically compiles custom vector SVG artwork and README for Diva143V GitHub profile.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
PROJECTS_DIR = os.path.join(ASSETS_DIR, "projects")


def fetch_github_data():
    """Fetch live public metrics for Diva143V with resilient fallback."""
    user_url = "https://api.github.com/users/Diva143V"
    repos_url = "https://api.github.com/users/Diva143V/repos?per_page=100"
    
    headers = {"User-Agent": "Nebula-Profile-Generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    data = {
        "login": "Diva143V",
        "name": "Diwakar Venkat Peddada",
        "public_repos": 23,
        "followers": 4,
        "total_stars": 16,
        "primary_languages": ["Python", "C#", "Rust", "TypeScript", "C++", "Java"],
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d")
    }

    try:
        req = urllib.request.Request(user_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                user_info = json.loads(resp.read().decode())
                data["public_repos"] = user_info.get("public_repos", data["public_repos"])
                data["followers"] = user_info.get("followers", data["followers"])
                
        req_repos = urllib.request.Request(repos_url, headers=headers)
        with urllib.request.urlopen(req_repos, timeout=5) as resp:
            if resp.status == 200:
                repos = json.loads(resp.read().decode())
                total_stars = sum(r.get("stargazers_count", 0) for r in repos)
                data["total_stars"] = max(total_stars, data["total_stars"])
                
                langs = {}
                for r in repos:
                    l = r.get("language")
                    if l:
                        langs[l] = langs.get(l, 0) + 1
                if langs:
                    sorted_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)
                    data["primary_languages"] = [l[0] for l in sorted_langs[:6]]
    except Exception as e:
        print(f"[Generator] Live API fetch notice (using verified baseline): {e}")

    return data


def create_hero_svg(path):
    """Generate Panoramic Cosmic Hero Banner with CSS animations (850x300)."""
    svg = """<svg width="850" height="300" viewBox="0 0 850 300" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="850" y2="300" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#030308"/>
      <stop offset="40%" stop-color="#080C1A"/>
      <stop offset="100%" stop-color="#050510"/>
    </linearGradient>
    <radialGradient id="neb1" cx="680" cy="80" r="220" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7B2CFF" stop-opacity="0.18"/>
      <stop offset="40%" stop-color="#3B82F6" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#030308" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="neb2" cx="140" cy="260" r="200" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#EC4899" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#030308" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="neb3" cx="420" cy="150" r="300" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#030308" stop-opacity="0"/>
    </radialGradient>
    <filter id="g" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <filter id="g2" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <style>
      @keyframes twinkle { 0%,100%{opacity:0.3} 50%{opacity:1} }
      @keyframes drift { 0%{transform:translateX(0)} 50%{transform:translateX(2px)} 100%{transform:translateX(0)} }
      @keyframes pulse { 0%,100%{opacity:0.4} 50%{opacity:0.8} }
      .star-a { animation: twinkle 3s ease-in-out infinite; }
      .star-b { animation: twinkle 4s ease-in-out infinite 1s; }
      .star-c { animation: twinkle 5s ease-in-out infinite 2s; }
      .orb { animation: pulse 6s ease-in-out infinite; }
      .drift { animation: drift 8s ease-in-out infinite; }
    </style>
  </defs>

  <!-- Deep space canvas -->
  <rect width="850" height="300" fill="url(#bg)"/>
  <rect width="850" height="300" fill="url(#neb1)"/>
  <rect width="850" height="300" fill="url(#neb2)"/>
  <rect width="850" height="300" fill="url(#neb3)"/>

  <!-- Dense starfield — 50+ stars at varied sizes and opacities -->
  <g>
    <!-- Bright primary stars -->
    <circle cx="78" cy="28" r="1.5" fill="#F8FAFC" class="star-a"/>
    <circle cx="210" cy="52" r="1.2" fill="#F8FAFC" opacity="0.9"/>
    <circle cx="345" cy="18" r="1" fill="#F8FAFC" class="star-b"/>
    <circle cx="520" cy="38" r="1.4" fill="#F8FAFC" opacity="0.8"/>
    <circle cx="680" cy="22" r="1.3" fill="#F8FAFC" class="star-c"/>
    <circle cx="790" cy="55" r="1" fill="#F8FAFC" opacity="0.7"/>
    <circle cx="130" cy="135" r="1.1" fill="#F8FAFC" class="star-b"/>
    <circle cx="420" cy="95" r="1.5" fill="#F8FAFC" class="star-a"/>
    <circle cx="590" cy="145" r="1.2" fill="#F8FAFC" opacity="0.6"/>
    <circle cx="815" cy="105" r="1" fill="#F8FAFC" class="star-c"/>
    <!-- Colored accent stars -->
    <circle cx="155" cy="78" r="1.5" fill="#22D3EE" opacity="0.7" class="star-c"/>
    <circle cx="460" cy="60" r="1.3" fill="#A855F7" opacity="0.8" class="star-a"/>
    <circle cx="720" cy="130" r="1.6" fill="#22D3EE" opacity="0.6" class="star-b"/>
    <circle cx="310" cy="175" r="1.2" fill="#EC4899" opacity="0.5" class="star-c"/>
    <circle cx="610" cy="65" r="1.4" fill="#A855F7" opacity="0.5"/>
    <!-- Dim background dust -->
    <circle cx="40" cy="90" r="0.8" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="95" cy="195" r="0.7" fill="#F8FAFC" opacity="0.25"/>
    <circle cx="180" cy="260" r="0.8" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="260" cy="110" r="0.6" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="370" cy="250" r="0.7" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="440" cy="210" r="0.8" fill="#F8FAFC" opacity="0.25"/>
    <circle cx="510" cy="280" r="0.6" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="560" cy="195" r="0.7" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="650" cy="260" r="0.8" fill="#F8FAFC" opacity="0.25"/>
    <circle cx="740" cy="185" r="0.7" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="805" cy="240" r="0.6" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="30" cy="250" r="0.7" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="295" cy="45" r="0.6" fill="#F8FAFC" opacity="0.25"/>
    <circle cx="755" cy="75" r="0.7" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="835" cy="170" r="0.6" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="485" cy="155" r="0.7" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="115" cy="45" r="0.6" fill="#F8FAFC" opacity="0.3"/>
    <circle cx="635" cy="190" r="0.7" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="390" cy="130" r="0.6" fill="#F8FAFC" opacity="0.15"/>
    <circle cx="550" cy="115" r="0.5" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="265" cy="225" r="0.5" fill="#F8FAFC" opacity="0.15"/>
    <circle cx="700" cy="275" r="0.6" fill="#F8FAFC" opacity="0.2"/>
    <circle cx="160" cy="175" r="0.5" fill="#F8FAFC" opacity="0.15"/>
  </g>

  <!-- Nebula glow cloud (soft diffuse light) -->
  <circle cx="700" cy="70" r="80" fill="#7B2CFF" opacity="0.06" filter="url(#g2)" class="orb"/>
  <circle cx="750" cy="100" r="50" fill="#22D3EE" opacity="0.05" filter="url(#g2)"/>
  <circle cx="120" cy="250" r="60" fill="#EC4899" opacity="0.04" filter="url(#g2)" class="orb"/>

  <!-- Constellation lines (connecting real stars) -->
  <g opacity="0.25" class="drift">
    <line x1="680" y1="22" x2="720" y2="130" stroke="#22D3EE" stroke-width="0.6"/>
    <line x1="720" y1="130" x2="790" y2="55" stroke="#22D3EE" stroke-width="0.6"/>
    <line x1="590" y1="145" x2="720" y2="130" stroke="#A855F7" stroke-width="0.5"/>
    <line x1="520" y1="38" x2="610" y2="65" stroke="#A855F7" stroke-width="0.4"/>
    <line x1="610" y1="65" x2="680" y2="22" stroke="#A855F7" stroke-width="0.4"/>
  </g>

  <!-- Orbital arc — a single elegant arc -->
  <g transform="translate(720, 95)" class="drift">
    <ellipse cx="0" cy="0" rx="70" ry="22" transform="rotate(-20)" stroke="#22D3EE" stroke-width="0.8" stroke-opacity="0.3" stroke-dasharray="4 6"/>
    <circle cx="45" cy="-15" r="2.5" fill="#22D3EE" opacity="0.8" filter="url(#g)"/>
    <circle cx="-38" cy="12" r="1.8" fill="#A855F7" opacity="0.6"/>
  </g>

  <!-- Location tag -->
  <g transform="translate(36, 28)">
    <rect width="168" height="20" rx="3" fill="#0B1024" fill-opacity="0.8" stroke="#1E293B" stroke-width="0.5"/>
    <circle cx="10" cy="10" r="2.5" fill="#22D3EE" class="star-a"/>
    <text x="20" y="14" font-family="ui-monospace, 'Cascadia Code', 'JetBrains Mono', monospace" font-size="9.5" font-weight="500" fill="#22D3EE" letter-spacing="0.8">17.68° N · 83.22° E</text>
  </g>

  <!-- Name -->
  <text x="36" y="98" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="36" font-weight="800" fill="#F8FAFC" letter-spacing="-0.5">Diwakar Venkat Peddada</text>

  <!-- Role line -->
  <text x="36" y="128" font-family="ui-monospace, 'Cascadia Code', 'JetBrains Mono', monospace" font-size="13" font-weight="500" fill="#94A3B8" letter-spacing="0.5">Software Engineer · AI Developer · CS '28 Andhra University</text>

  <!-- One-liner -->
  <text x="36" y="172" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="14" fill="#64748B">I build software that has to keep up with something happening live —</text>
  <text x="36" y="194" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="14" fill="#64748B">speech turning into subtitles, papers turning into evidence,</text>
  <text x="36" y="216" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="14" fill="#64748B">and interfaces that stay quick under load.</text>

  <!-- Factual pills -->
  <g transform="translate(36, 248)">
    <rect width="100" height="22" rx="4" fill="#0B1024" fill-opacity="0.8" stroke="#1E293B" stroke-width="0.5"/>
    <text x="50" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#22D3EE">AI Intern</text>

    <rect x="108" y="0" width="140" height="22" rx="4" fill="#0B1024" fill-opacity="0.8" stroke="#1E293B" stroke-width="0.5"/>
    <text x="178" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#A855F7">Aegion Dynamic Solutions</text>

    <rect x="256" y="0" width="120" height="22" rx="4" fill="#0B1024" fill-opacity="0.8" stroke="#1E293B" stroke-width="0.5"/>
    <text x="316" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#EC4899">185K community</text>

    <rect x="384" y="0" width="105" height="22" rx="4" fill="#0B1024" fill-opacity="0.8" stroke="#1E293B" stroke-width="0.5"/>
    <text x="436" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#3B82F6">1st place winner</text>
  </g>

  <!-- Thin border -->
  <rect x="0.5" y="0.5" width="849" height="299" rx="12" stroke="#1E293B" stroke-width="0.5"/>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def create_statistics_svg(path, data):
    """Generate Local Dynamic Statistics Panel (850x140)."""
    repos_cnt = data.get("public_repos", 23)
    stars_cnt = data.get("total_stars", 16)
    
    svg = f"""<svg width="850" height="140" viewBox="0 0 850 140" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="850" y2="140" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#080C1A"/>
      <stop offset="100%" stop-color="#050510"/>
    </linearGradient>
    <style>
      @keyframes countPulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.7}} }}
      .live-dot {{ animation: countPulse 2s ease-in-out infinite; }}
    </style>
  </defs>

  <rect width="850" height="140" rx="10" fill="url(#sbg)"/>
  <rect x="0.5" y="0.5" width="849" height="139" rx="9.5" stroke="#1E293B" stroke-width="0.5"/>

  <!-- Header bar -->
  <line x1="24" y1="32" x2="826" y2="32" stroke="#1E293B" stroke-width="0.5"/>
  <circle cx="34" cy="18" r="3" fill="#22D3EE" class="live-dot"/>
  <text x="44" y="22" font-family="ui-monospace, monospace" font-size="10" font-weight="600" fill="#64748B" letter-spacing="1">GITHUB PUBLIC METRICS</text>

  <!-- Metric 1 -->
  <g transform="translate(28, 46)">
    <rect width="186" height="76" rx="6" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="14" y="24" font-family="ui-monospace, monospace" font-size="9.5" fill="#64748B" letter-spacing="0.5">REPOSITORIES</text>
    <text x="14" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="28" font-weight="800" fill="#F8FAFC">{repos_cnt}</text>
    <text x="52" y="56" font-family="ui-monospace, monospace" font-size="10" fill="#475569">public</text>
  </g>

  <!-- Metric 2 -->
  <g transform="translate(226, 46)">
    <rect width="186" height="76" rx="6" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="14" y="24" font-family="ui-monospace, monospace" font-size="9.5" fill="#64748B" letter-spacing="0.5">STARS EARNED</text>
    <text x="14" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="28" font-weight="800" fill="#22D3EE">{stars_cnt}</text>
    <text x="46" y="56" font-family="ui-monospace, monospace" font-size="10" fill="#475569">across projects</text>
  </g>

  <!-- Metric 3 -->
  <g transform="translate(424, 46)">
    <rect width="186" height="76" rx="6" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="14" y="24" font-family="ui-monospace, monospace" font-size="9.5" fill="#64748B" letter-spacing="0.5">LANGUAGES</text>
    <text x="14" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="28" font-weight="800" fill="#A855F7">6</text>
    <text x="30" y="56" font-family="ui-monospace, monospace" font-size="10" fill="#475569">primary</text>
    <text x="14" y="68" font-family="ui-monospace, monospace" font-size="8.5" fill="#475569">Python · C# · Rust · TS · C++ · Java</text>
  </g>

  <!-- Metric 4 -->
  <g transform="translate(622, 46)">
    <rect width="200" height="76" rx="6" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="14" y="24" font-family="ui-monospace, monospace" font-size="9.5" fill="#64748B" letter-spacing="0.5">COMPETITION</text>
    <text x="14" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="24" font-weight="800" fill="#EC4899">1st Place</text>
    <text x="14" y="68" font-family="ui-monospace, monospace" font-size="8.5" fill="#475569">HackMe · C++ optimization</text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def create_tech_constellation_svg(path):
    """Generate Sleek Multi-Row Technology Constellation (850x230)."""
    svg = """<svg width="850" height="230" viewBox="0 0 850 230" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="850" y2="230" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#050510"/>
      <stop offset="100%" stop-color="#080C1A"/>
    </linearGradient>
    <style>
      @keyframes fadeIn { 0%{opacity:0.5} 100%{opacity:1} }
      .tech-tag { animation: fadeIn 0.3s ease-out forwards; }
    </style>
  </defs>

  <rect width="850" height="230" rx="10" fill="url(#tbg)"/>
  <rect x="0.5" y="0.5" width="849" height="229" rx="9.5" stroke="#1E293B" stroke-width="0.5"/>

  <!-- Row 1: Systems -->
  <g transform="translate(28, 20)">
    <circle cx="6" cy="8" r="3.5" fill="#22D3EE"/>
    <text x="16" y="12" font-family="ui-monospace, monospace" font-size="10" font-weight="600" fill="#22D3EE" letter-spacing="0.5">SYSTEMS &amp; REAL-TIME</text>
    <g transform="translate(0, 22)">
      <rect x="0" y="0" width="38" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="19" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#F8FAFC">C#</text>
      <rect x="44" y="0" width="42" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="65" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#F8FAFC">C++</text>
      <rect x="92" y="0" width="84" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="134" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Windows APIs</text>
      <rect x="182" y="0" width="82" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="223" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Live Captions</text>
      <rect x="270" y="0" width="80" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="310" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Overlay GUIs</text>
    </g>
  </g>

  <!-- Row 2: AI & Biomedical -->
  <g transform="translate(28, 72)">
    <circle cx="6" cy="8" r="3.5" fill="#EC4899"/>
    <text x="16" y="12" font-family="ui-monospace, monospace" font-size="10" font-weight="600" fill="#EC4899" letter-spacing="0.5">BIOMEDICAL AI &amp; RESEARCH</text>
    <g transform="translate(0, 22)">
      <rect x="0" y="0" width="55" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="27" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#F8FAFC">Python</text>
      <rect x="61" y="0" width="58" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="90" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">RAG</text>
      <rect x="125" y="0" width="80" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="165" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">ChromaDB</text>
      <rect x="211" y="0" width="58" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="240" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Ollama</text>
      <rect x="275" y="0" width="55" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="302" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Reflex</text>
      <rect x="336" y="0" width="104" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="388" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Mixture-of-LLMs</text>
      <rect x="446" y="0" width="80" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="486" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Neoantigen</text>
    </g>
  </g>

  <!-- Row 3: Knowledge Graphs & Security -->
  <g transform="translate(28, 124)">
    <circle cx="6" cy="8" r="3.5" fill="#A855F7"/>
    <text x="16" y="12" font-family="ui-monospace, monospace" font-size="10" font-weight="600" fill="#A855F7" letter-spacing="0.5">KNOWLEDGE GRAPHS &amp; SECURITY</text>
    <g transform="translate(0, 22)">
      <rect x="0" y="0" width="45" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="22" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#F8FAFC">Rust</text>
      <rect x="51" y="0" width="40" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="71" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#F8FAFC">MCP</text>
      <rect x="97" y="0" width="58" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="126" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Docker</text>
      <rect x="161" y="0" width="118" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="220" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Think-on-Graph (ToG)</text>
      <rect x="285" y="0" width="78" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="324" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Crates.io CI</text>
    </g>
  </g>

  <!-- Row 4: Web & Cloud -->
  <g transform="translate(28, 176)">
    <circle cx="6" cy="8" r="3.5" fill="#3B82F6"/>
    <text x="16" y="12" font-family="ui-monospace, monospace" font-size="10" font-weight="600" fill="#3B82F6" letter-spacing="0.5">WEB &amp; CLOUD</text>
    <g transform="translate(0, 22)">
      <rect x="0" y="0" width="82" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="41" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">TypeScript</text>
      <rect x="88" y="0" width="52" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="114" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10" fill="#F8FAFC">React</text>
      <rect x="146" y="0" width="58" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="175" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Node.js</text>
      <rect x="210" y="0" width="58" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="239" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Canvas</text>
      <rect x="274" y="0" width="94" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="321" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Google Cloud</text>
      <rect x="374" y="0" width="80" height="20" rx="4" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
      <text x="414" y="14" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">GitHub CI</text>
    </g>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def create_project_cards():
    """Generate high-contrast, animated project cards for LiveSubs, Griffin, Knox, and SyGriffin."""
    # 1. LiveSubs
    livesubs_svg = """<svg width="850" height="130" viewBox="0 0 850 130" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes wave { 0%,100%{transform:scaleY(1)} 50%{transform:scaleY(0.6)} }
      .bar1{animation:wave 1.2s ease-in-out infinite}
      .bar2{animation:wave 1.2s ease-in-out infinite 0.15s}
      .bar3{animation:wave 1.2s ease-in-out infinite 0.3s}
      .bar4{animation:wave 1.2s ease-in-out infinite 0.45s}
      .bar5{animation:wave 1.2s ease-in-out infinite 0.6s}
      .bar6{animation:wave 1.2s ease-in-out infinite 0.75s}
    </style>
  </defs>

  <rect width="850" height="130" rx="8" fill="#080C1A"/>
  <rect x="0.5" y="0.5" width="849" height="129" rx="7.5" stroke="#1E293B" stroke-width="0.5"/>
  <!-- Left accent -->
  <rect width="3" height="130" fill="#22D3EE" rx="0"/>

  <!-- Title row -->
  <text x="22" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="18" font-weight="800" fill="#F8FAFC">LiveSubs</text>
  <text x="120" y="28" font-family="ui-monospace, monospace" font-size="9" font-weight="600" fill="#22D3EE" letter-spacing="0.5">SHIPPED · 7 ★</text>

  <!-- One-line description -->
  <text x="22" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">Real-time subtitle &amp; translation overlay for Windows. Hooks Live Captions,</text>
  <text x="22" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">translates via LLM or classic APIs, renders always-on-top over any app.</text>

  <!-- Tech tags -->
  <g transform="translate(22, 82)">
    <rect x="0" y="0" width="34" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="17" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">C#</text>
    <rect x="40" y="0" width="42" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="61" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">.NET</text>
    <rect x="88" y="0" width="94" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="135" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Live Captions</text>
    <rect x="188" y="0" width="78" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="227" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Translation</text>
    <rect x="272" y="0" width="58" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="301" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">WPF</text>
  </g>

  <!-- Downloads pill -->
  <g transform="translate(22, 108)">
    <rect width="140" height="16" rx="3" fill="#22D3EE" fill-opacity="0.1" stroke="#22D3EE" stroke-width="0.5" stroke-opacity="0.3"/>
    <text x="70" y="12" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" fill="#22D3EE">↓ Releases available</text>
  </g>

  <!-- Animated waveform motif -->
  <g transform="translate(740, 30)">
    <rect x="0" y="20" width="4" height="50" rx="2" fill="#22D3EE" opacity="0.5" class="bar1" transform-origin="2 45"/>
    <rect x="10" y="10" width="4" height="70" rx="2" fill="#22D3EE" opacity="0.7" class="bar2" transform-origin="12 45"/>
    <rect x="20" y="0" width="4" height="90" rx="2" fill="#22D3EE" opacity="0.9" class="bar3" transform-origin="22 45"/>
    <rect x="30" y="15" width="4" height="60" rx="2" fill="#22D3EE" opacity="0.6" class="bar4" transform-origin="32 45"/>
    <rect x="40" y="5" width="4" height="80" rx="2" fill="#22D3EE" opacity="0.8" class="bar5" transform-origin="42 45"/>
    <rect x="50" y="25" width="4" height="40" rx="2" fill="#22D3EE" opacity="0.4" class="bar6" transform-origin="52 45"/>
  </g>
</svg>"""
    with open(os.path.join(PROJECTS_DIR, "livesubs.svg"), "w", encoding="utf-8") as f:
        f.write(livesubs_svg)
    print("[Generator] Created livesubs.svg")

    # 2. Griffin Bio
    griffin_svg = """<svg width="850" height="130" viewBox="0 0 850 130" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes nodeGlow { 0%,100%{opacity:0.4} 50%{opacity:1} }
      .n1{animation:nodeGlow 2.5s ease-in-out infinite}
      .n2{animation:nodeGlow 2.5s ease-in-out infinite 0.8s}
      .n3{animation:nodeGlow 2.5s ease-in-out infinite 1.6s}
    </style>
  </defs>

  <rect width="850" height="130" rx="8" fill="#080C1A"/>
  <rect x="0.5" y="0.5" width="849" height="129" rx="7.5" stroke="#1E293B" stroke-width="0.5"/>
  <rect width="3" height="130" fill="#EC4899" rx="0"/>

  <text x="22" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="18" font-weight="800" fill="#F8FAFC">Griffin Bio</text>
  <text x="128" y="28" font-family="ui-monospace, monospace" font-size="9" font-weight="600" fill="#EC4899" letter-spacing="0.5">RESEARCH · 2 ★</text>

  <text x="22" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">Scientific evidence synthesis &amp; contradiction workbench. Ingests from 10</text>
  <text x="22" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">biomedical collectors, runs Mixture-of-LLMs claim extraction &amp; ranking.</text>

  <g transform="translate(22, 82)">
    <rect x="0" y="0" width="55" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="27" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Python</text>
    <rect x="61" y="0" width="94" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="108" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">ChromaDB RAG</text>
    <rect x="161" y="0" width="58" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="190" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Ollama</text>
    <rect x="225" y="0" width="55" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="252" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Reflex</text>
    <rect x="286" y="0" width="94" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="333" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" fill="#F8FAFC">10 Collectors</text>
  </g>

  <!-- Neural network motif — animated nodes -->
  <g transform="translate(720, 25)">
    <line x1="10" y1="20" x2="55" y2="10" stroke="#EC4899" stroke-width="0.8" opacity="0.3"/>
    <line x1="10" y1="20" x2="30" y2="55" stroke="#EC4899" stroke-width="0.8" opacity="0.3"/>
    <line x1="55" y1="10" x2="80" y2="45" stroke="#EC4899" stroke-width="0.8" opacity="0.3"/>
    <line x1="30" y1="55" x2="80" y2="45" stroke="#EC4899" stroke-width="0.8" opacity="0.3"/>
    <line x1="55" y1="10" x2="90" y2="15" stroke="#EC4899" stroke-width="0.6" opacity="0.2"/>
    <line x1="80" y1="45" x2="100" y2="65" stroke="#EC4899" stroke-width="0.6" opacity="0.2"/>
    <circle cx="10" cy="20" r="5" fill="#EC4899" class="n1"/>
    <circle cx="55" cy="10" r="4" fill="#EC4899" class="n2"/>
    <circle cx="30" cy="55" r="5.5" fill="#EC4899" class="n3"/>
    <circle cx="80" cy="45" r="4.5" fill="#EC4899" class="n1"/>
    <circle cx="90" cy="15" r="2.5" fill="#EC4899" opacity="0.3"/>
    <circle cx="100" cy="65" r="2.5" fill="#EC4899" opacity="0.3"/>
  </g>
</svg>"""
    with open(os.path.join(PROJECTS_DIR, "griffin.svg"), "w", encoding="utf-8") as f:
        f.write(griffin_svg)
    print("[Generator] Created griffin.svg")

    # 3. Knox
    knox_svg = """<svg width="850" height="130" viewBox="0 0 850 130" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes lockPulse { 0%,100%{opacity:0.5} 50%{opacity:1} }
      .lock { animation: lockPulse 3s ease-in-out infinite; }
    </style>
  </defs>

  <rect width="850" height="130" rx="8" fill="#080C1A"/>
  <rect x="0.5" y="0.5" width="849" height="129" rx="7.5" stroke="#1E293B" stroke-width="0.5"/>
  <rect width="3" height="130" fill="#A855F7" rx="0"/>

  <text x="22" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="18" font-weight="800" fill="#F8FAFC">Knox</text>
  <text x="70" y="28" font-family="ui-monospace, monospace" font-size="9" font-weight="600" fill="#A855F7" letter-spacing="0.5">MCP VAULT · 2 ★</text>

  <text x="22" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">Rust MCP memory server for AI agents. Session isolation, secure persistence,</text>
  <text x="22" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">cryptographic boundaries, and automated CI/CD releases to Crates.io.</text>

  <g transform="translate(22, 82)">
    <rect x="0" y="0" width="45" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="22" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Rust</text>
    <rect x="51" y="0" width="82" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="92" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">TypeScript</text>
    <rect x="139" y="0" width="94" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="186" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">MCP Protocol</text>
    <rect x="239" y="0" width="72" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="275" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Crates.io</text>
    <rect x="317" y="0" width="78" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="356" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">GitHub CI</text>
  </g>

  <!-- Shield motif — animated lock -->
  <g transform="translate(730, 20)">
    <polygon points="40,5 70,18 70,52 40,70 10,52 10,18" fill="none" stroke="#A855F7" stroke-width="1.2" opacity="0.4"/>
    <polygon points="40,15 60,24 60,46 40,58 20,46 20,24" fill="none" stroke="#A855F7" stroke-width="0.8" opacity="0.25" stroke-dasharray="3 3"/>
    <circle cx="40" cy="36" r="6" fill="#A855F7" class="lock"/>
    <rect x="36" y="40" width="8" height="6" rx="1" fill="#A855F7" opacity="0.6"/>
  </g>
</svg>"""
    with open(os.path.join(PROJECTS_DIR, "knox.svg"), "w", encoding="utf-8") as f:
        f.write(knox_svg)
    print("[Generator] Created knox.svg")

    # 4. SyGriffin
    sygriffin_svg = """<svg width="850" height="130" viewBox="0 0 850 130" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes dnaHelix { 0%,100%{opacity:0.3} 50%{opacity:0.9} }
      .h1{animation:dnaHelix 2s ease-in-out infinite}
      .h2{animation:dnaHelix 2s ease-in-out infinite 0.5s}
      .h3{animation:dnaHelix 2s ease-in-out infinite 1s}
      .h4{animation:dnaHelix 2s ease-in-out infinite 1.5s}
    </style>
  </defs>

  <rect width="850" height="130" rx="8" fill="#080C1A"/>
  <rect x="0.5" y="0.5" width="849" height="129" rx="7.5" stroke="#1E293B" stroke-width="0.5"/>
  <rect width="3" height="130" fill="#F472B6" rx="0"/>

  <text x="22" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="18" font-weight="800" fill="#F8FAFC">SyGriffin</text>
  <text x="128" y="28" font-family="ui-monospace, monospace" font-size="9" font-weight="600" fill="#F472B6" letter-spacing="0.5">BIOINFORMATICS · 2 ★</text>

  <text x="22" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">CLI-first AI bioinformatics platform for neoantigen discovery. Analyzes tumor</text>
  <text x="22" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="#94A3B8">VCF files, predicts vaccine-relevant peptide candidates with transparent scoring.</text>

  <g transform="translate(22, 82)">
    <rect x="0" y="0" width="55" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="27" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">Python</text>
    <rect x="61" y="0" width="38" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="80" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="#F8FAFC">R</text>
    <rect x="105" y="0" width="82" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="146" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">TypeScript</text>
    <rect x="193" y="0" width="82" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="234" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">Neoantigen</text>
    <rect x="281" y="0" width="82" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="322" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">VCF Pipeline</text>
    <rect x="369" y="0" width="58" height="18" rx="3" fill="#0B1024" stroke="#1E293B" stroke-width="0.5"/>
    <text x="398" y="13" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="#F8FAFC">LaTeX</text>
  </g>

  <!-- DNA helix / peptide chain motif -->
  <g transform="translate(720, 15)">
    <!-- Double helix strands -->
    <path d="M 10,10 Q 25,25 40,10 Q 55,-5 70,10 Q 85,25 100,10" fill="none" stroke="#F472B6" stroke-width="1.2" opacity="0.5"/>
    <path d="M 10,10 Q 25,-5 40,10 Q 55,25 70,10 Q 85,-5 100,10" fill="none" stroke="#F472B6" stroke-width="1.2" opacity="0.5"/>
    <!-- Rungs -->
    <line x1="25" y1="4" x2="25" y2="16" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
    <line x1="40" y1="4" x2="40" y2="16" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
    <line x1="55" y1="4" x2="55" y2="16" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
    <line x1="70" y1="4" x2="70" y2="16" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
    <line x1="85" y1="4" x2="85" y2="16" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
    <!-- Animated base pair nodes -->
    <circle cx="25" cy="4" r="3" fill="#F472B6" class="h1"/>
    <circle cx="40" cy="16" r="3" fill="#F472B6" class="h2"/>
    <circle cx="55" cy="4" r="3" fill="#F472B6" class="h3"/>
    <circle cx="70" cy="16" r="3" fill="#F472B6" class="h4"/>
    <circle cx="85" cy="4" r="2.5" fill="#F472B6" class="h1"/>

    <!-- Second row offset -->
    <g transform="translate(0, 45)">
      <path d="M 10,10 Q 25,25 40,10 Q 55,-5 70,10 Q 85,25 100,10" fill="none" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
      <path d="M 10,10 Q 25,-5 40,10 Q 55,25 70,10 Q 85,-5 100,10" fill="none" stroke="#F472B6" stroke-width="0.8" opacity="0.3"/>
      <circle cx="30" cy="10" r="2" fill="#F472B6" opacity="0.3"/>
      <circle cx="60" cy="10" r="2" fill="#F472B6" opacity="0.3"/>
      <circle cx="90" cy="10" r="2" fill="#F472B6" opacity="0.2"/>
    </g>
  </g>
</svg>"""
    with open(os.path.join(PROJECTS_DIR, "sygriffin.svg"), "w", encoding="utf-8") as f:
        f.write(sygriffin_svg)
    print("[Generator] Created sygriffin.svg")


def create_footer_svg(path):
    """Generate Minimalist Cosmic Footer (850x90)."""
    svg = """<svg width="850" height="90" viewBox="0 0 850 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.4} }
      .beacon { animation: blink 2s ease-in-out infinite; }
    </style>
  </defs>

  <rect width="850" height="90" rx="8" fill="#080C1A"/>
  <rect x="0.5" y="0.5" width="849" height="89" rx="7.5" stroke="#1E293B" stroke-width="0.5"/>

  <circle cx="30" cy="24" r="3" fill="#22D3EE" class="beacon"/>
  <text x="42" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="15" font-weight="700" fill="#F8FAFC">Let's build something.</text>

  <text x="30" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12" fill="#64748B">Open for internships, research collaborations, and projects that need someone who will actually finish them.</text>

  <text x="30" y="74" font-family="ui-monospace, monospace" font-size="10" fill="#475569">diwa.p2007@gmail.com · github.com/Diva143V · linkedin · x.com/Diva_2007_</text>

  <!-- Small constellation -->
  <g transform="translate(760, 20)" opacity="0.4">
    <circle cx="10" cy="10" r="2" fill="#22D3EE" class="beacon"/>
    <circle cx="45" cy="25" r="1.5" fill="#A855F7"/>
    <circle cx="25" cy="45" r="2" fill="#EC4899"/>
    <line x1="10" y1="10" x2="45" y2="25" stroke="#22D3EE" stroke-width="0.5"/>
    <line x1="10" y1="10" x2="25" y2="45" stroke="#EC4899" stroke-width="0.5"/>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def generate_readme(data):
    """Generate master README.md adhering strictly to no-slop principles and verified audit truth."""
    readme_path = os.path.join(ROOT_DIR, "README.md")
    
    content = """<div align="center">
<img src="assets/hero.svg" alt="Diwakar Venkat Peddada — Software Engineer" width="100%">
</div>

---

## About

I'm **Diwakar Venkat Peddada** — I go by Diva. I study CS at Andhra University and work as an AI developer intern at Aegion Dynamic Solutions.

I like problems where the answer has to arrive while you're still watching: captions that keep pace with a speaker, a pipeline that reads thousands of papers and tells you where they disagree, an overlay that sits on top of your video call and just works.

I started on the front end — rebuilding React interfaces at Aegion, learning to measure something before claiming it got faster. Since then I've been working further down the stack: Windows overlays in C#, embeddings and retrieval for research data, MCP servers in Rust, and a bioinformatics platform that predicts neoantigen candidates from tumor VCF files.

Outside of code, I moderated a 185,000-member community for Mecha Break, which taught me to write for people who haven't read the manual.

---

## Stats

<div align="center">
<img src="assets/statistics.svg" alt="GitHub metrics" width="100%">
</div>

---

## Stack

Everything listed here is backed by repository source code, not résumé padding.

<div align="center">
<img src="assets/tech-constellation.svg" alt="Technology stack" width="100%">
</div>

<details>
<summary><b>Where each technology is used</b></summary>
<br>

| Domain | Technologies | Evidence |
|---|---|---|
| **Systems & real-time** | C#, .NET, C++, Windows APIs, Live Captions | [LiveSubs](https://github.com/Diva143V/LiveSubs), HackMe solver |
| **Biomedical AI** | Python, ChromaDB, Ollama, RAG, Mixture-of-LLMs, Reflex | [Griffin](https://github.com/Diva143V/Griffin), [SyGriffin](https://github.com/Diva143V/SyGriffin) |
| **Knowledge graphs & security** | Rust, MCP, Think-on-Graph, Docker | [Knox](https://github.com/Diva143V/Knox), [Kg-Library-API](https://github.com/Diva143V/Kg-Library-API), [Laya-KG](https://github.com/Diva143V/Laya-KG) |
| **Web & cloud** | TypeScript, React, Node.js, Canvas, Google Cloud, GitHub CI | [chatstream](https://github.com/Diva143V/chatstream), [myselfdiva](https://github.com/Diva143V/myselfdiva) |

</details>

---

## Projects

### LiveSubs

<a href="https://github.com/Diva143V/LiveSubs">
<img src="assets/projects/livesubs.svg" alt="LiveSubs" width="100%">
</a>

Real-time subtitle and translation overlay for Windows. Hooks into Live Captions, translates through LLM or traditional APIs, renders always-on-top subtitles over any app — calls, streams, lectures. Ships with [downloadable releases](https://github.com/Diva143V/LiveSubs/releases).

---

### Griffin Bio

<a href="https://github.com/Diva143V/Griffin">
<img src="assets/projects/griffin.svg" alt="Griffin Bio" width="100%">
</a>

Scientific evidence synthesis workbench. Collects from 10 biomedical sources (PubMed, Europe PMC, ChEMBL, UniProt, OpenAlex, and more), deduplicates, embeds in ChromaDB, then runs a Mixture-of-LLMs pipeline to extract claims, rank evidence, and flag contradictions. Live dashboard via Reflex.

---

### Knox

<a href="https://github.com/Diva143V/Knox">
<img src="assets/projects/knox.svg" alt="Knox" width="100%">
</a>

Rust-based Model Context Protocol (MCP) memory server for AI agents. Provides session isolation, cryptographic boundaries, and secure persistence. Published to Crates.io with automated CI/CD releases.

---

### SyGriffin

<a href="https://github.com/Diva143V/SyGriffin">
<img src="assets/projects/sygriffin.svg" alt="SyGriffin" width="100%">
</a>

CLI-first AI bioinformatics platform for neoantigen discovery. Takes tumor VCF files, predicts vaccine-relevant peptide candidates, ranks them with transparent scoring, and generates reproducible LaTeX research reports. For research use only — not a diagnostic tool.

---

## Experience

**AI Developer Intern** — Aegion Dynamic Solutions `Jul 2026 — Present`
Building AI-powered features and LLM integrations that ship into production.

**Front-End Developer Intern** — Aegion Dynamic Solutions `Aug — Oct 2025`
Rebuilt React interfaces, cut unnecessary re-renders, tightened API integration.

**Community Moderator** — Mecha Break / Amazing Seasun Games `Mar 2024 — Jul 2025`
Managed 185,000+ members. Compiled player feedback into actionable developer reports.

### Credentials
- 🥇 **1st Place** — HackMe Problem Statement Solver (2024)
- JPMorgan Chase & Co. Software Engineering Simulation
- Google Cloud Compute Fundamentals
- HackerRank C & C++ Certification

---

## Connect

<div align="center">
<a href="mailto:diwa.p2007@gmail.com">
<img src="assets/footer.svg" alt="Contact" width="100%">
</a>
<br><br>
<a href="https://myselfdiva.netlify.app/">Portfolio</a> · <a href="https://linkedin.com/in/diwakar-venkat-peddada-66aa30229/">LinkedIn</a> · <a href="https://x.com/Diva_2007_">X</a> · <a href="mailto:diwa.p2007@gmail.com">diwa.p2007@gmail.com</a>
</div>
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Generator] Created {readme_path}")


def main():
    print("[Generator] Starting NEBULA / 01 Generation Pipeline...")
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    
    data = fetch_github_data()
    print(f"[Generator] Data: {data['public_repos']} repos, {data['total_stars']} stars, {data['followers']} followers.")
    
    create_hero_svg(os.path.join(ASSETS_DIR, "hero.svg"))
    create_statistics_svg(os.path.join(ASSETS_DIR, "statistics.svg"), data)
    create_tech_constellation_svg(os.path.join(ASSETS_DIR, "tech-constellation.svg"))
    create_project_cards()
    create_footer_svg(os.path.join(ASSETS_DIR, "footer.svg"))
    
    generate_readme(data)
    print("[Generator] Pipeline completed successfully!")


if __name__ == "__main__":
    main()
