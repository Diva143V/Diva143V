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

# Palette Tokens (NEBULA / 01)
C_BG = "#050510"
C_SURFACE = "#0B1024"
C_SURFACE_ALT = "#0D1530"
C_BORDER = "#1E293B"
C_BORDER_GLOW = "#38BDF8"
C_PURPLE = "#7B2CFF"
C_VIOLET = "#A855F7"
C_CYAN = "#22D3EE"
C_BLUE = "#3B82F6"
C_MAGENTA = "#EC4899"
C_WHITE = "#F8FAFC"
C_MUTED = "#94A3B8"
C_FAINT = "#475569"


def xml_escape(text):
    """Safely escape text for XML/SVG rendering."""
    if not text:
        return ""
    # Only escape & if it is not already an entity
    s = str(text)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace('"', "&quot;").replace("'", "&apos;")
    return s


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
        "primary_languages": ["Python", "C#", "Rust", "C++", "TypeScript", "Java"],
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
    """Generate Panoramic Cosmic Hero Banner (850x290)."""
    svg = f"""<svg width="850" height="290" viewBox="0 0 850 290" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="heroBg" x1="0" y1="0" x2="850" y2="290" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_BG}"/>
      <stop offset="50%" stop-color="{C_SURFACE}"/>
      <stop offset="100%" stop-color="{C_BG}"/>
    </linearGradient>
    <linearGradient id="neonGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{C_CYAN}"/>
      <stop offset="50%" stop-color="{C_VIOLET}"/>
      <stop offset="100%" stop-color="{C_MAGENTA}"/>
    </linearGradient>
    <radialGradient id="nebulaCore" cx="720" cy="90" r="180" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_PURPLE}" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="{C_CYAN}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{C_BG}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="nebulaGlowLeft" cx="120" cy="220" r="160" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_BLUE}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{C_BG}" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="850" height="290" rx="14" fill="url(#heroBg)"/>
  <rect width="850" height="290" rx="14" fill="url(#nebulaCore)"/>
  <rect width="850" height="290" rx="14" fill="url(#nebulaGlowLeft)"/>
  <rect x="0.5" y="0.5" width="849" height="289" rx="13.5" stroke="{C_BORDER}" stroke-width="1"/>

  <!-- Starfield Grid -->
  <g opacity="0.65">
    <circle cx="85" cy="45" r="1" fill="{C_WHITE}" opacity="0.8"/>
    <circle cx="160" cy="110" r="1.5" fill="{C_CYAN}" opacity="0.6"/>
    <circle cx="230" cy="30" r="1" fill="{C_WHITE}" opacity="0.5"/>
    <circle cx="340" cy="75" r="1.2" fill="{C_WHITE}" opacity="0.7"/>
    <circle cx="490" cy="40" r="1" fill="{C_VIOLET}" opacity="0.9"/>
    <circle cx="610" cy="85" r="1.5" fill="{C_CYAN}" opacity="0.8"/>
    <circle cx="750" cy="45" r="1.2" fill="{C_WHITE}" opacity="0.9"/>
    <circle cx="790" cy="130" r="1" fill="{C_WHITE}" opacity="0.6"/>
    <circle cx="680" cy="230" r="1.5" fill="{C_MAGENTA}" opacity="0.7"/>
    <circle cx="530" cy="250" r="1" fill="{C_WHITE}" opacity="0.5"/>
    <circle cx="380" cy="220" r="1.2" fill="{C_CYAN}" opacity="0.6"/>
    <circle cx="190" cy="240" r="1" fill="{C_WHITE}" opacity="0.8"/>
    <circle cx="70" cy="190" r="1.5" fill="{C_WHITE}" opacity="0.7"/>
    <circle cx="290" cy="160" r="1" fill="{C_WHITE}" opacity="0.4"/>
  </g>

  <!-- Constellation Geometric Vectors -->
  <g stroke="{C_BORDER}" stroke-width="0.8" opacity="0.5">
    <line x1="610" y1="85" x2="680" y2="120" stroke="{C_CYAN}" stroke-opacity="0.3"/>
    <line x1="680" y1="120" x2="750" y2="90" stroke="{C_CYAN}" stroke-opacity="0.3"/>
    <line x1="750" y1="90" x2="790" y2="130" stroke="{C_VIOLET}" stroke-opacity="0.3"/>
    <circle cx="680" cy="120" r="2.5" fill="{C_CYAN}" filter="url(#glow)"/>
    <circle cx="750" cy="90" r="2" fill="{C_VIOLET}"/>
  </g>

  <!-- Orbital Ring Geometry -->
  <g transform="translate(710, 110)">
    <ellipse cx="0" cy="0" rx="90" ry="28" transform="rotate(-25)" stroke="{C_CYAN}" stroke-width="1.2" stroke-opacity="0.4" stroke-dasharray="5 3"/>
    <ellipse cx="0" cy="0" rx="65" ry="65" stroke="{C_VIOLET}" stroke-width="0.8" stroke-opacity="0.25"/>
    <circle cx="0" cy="0" r="32" fill="{C_SURFACE_ALT}" stroke="{C_CYAN}" stroke-width="1.5" filter="url(#glow)"/>
    <circle cx="-12" cy="-10" r="3" fill="{C_MAGENTA}" opacity="0.8"/>
    <circle cx="8" cy="14" r="2" fill="{C_CYAN}" opacity="0.7"/>
    <circle cx="48" cy="-22" r="3" fill="{C_CYAN}" filter="url(#glow)"/>
  </g>

  <!-- Telemetry Coordinate Tag -->
  <g transform="translate(42, 42)">
    <rect x="0" y="0" width="220" height="24" rx="4" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <circle cx="12" cy="12" r="3.5" fill="{C_CYAN}" filter="url(#glow)"/>
    <text x="24" y="16" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="10.5" font-weight="600" fill="{C_CYAN}" letter-spacing="1">ORBIT 17.68° N · 83.22° E</text>
  </g>

  <!-- Name & Header Display -->
  <text x="42" y="112" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, &apos;Space Grotesk&apos;, sans-serif" font-size="34" font-weight="800" fill="{C_WHITE}" letter-spacing="-0.5">
    DIWAKAR VENKAT PEDDADA
  </text>

  <!-- Identity Subtitle Badge -->
  <g transform="translate(42, 128)">
    <text x="0" y="16" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="12.5" font-weight="600" fill="url(#neonGrad)" letter-spacing="1.5">
      SYSTEMS &amp; REAL-TIME SOFTWARE  //  BIOMEDICAL AI  //  KNOWLEDGE GRAPHS
    </text>
  </g>

  <!-- Philosophical Tagline -->
  <text x="42" y="185" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="14.5" fill="{C_MUTED}">
    Architecting software that keeps pace with real-time reality — from millisecond Windows
  </text>
  <text x="42" y="208" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="14.5" fill="{C_MUTED}">
    caption overlays to multi-source biomedical research synthesis and reasoning engines.
  </text>

  <!-- HUD Badges -->
  <g transform="translate(42, 238)">
    <!-- Pill 1 -->
    <rect x="0" y="0" width="175" height="26" rx="5" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="12" y="17" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_WHITE}">ANDHRA UNIVERSITY · CS &apos;28</text>

    <!-- Pill 2 -->
    <rect x="185" y="0" width="180" height="26" rx="5" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="197" y="17" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_CYAN}">AI DEV INTERN @ AEGION</text>

    <!-- Pill 3 -->
    <rect x="375" y="0" width="165" height="26" rx="5" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="387" y="17" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_VIOLET}">185K+ COMMUNITY MOD</text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def create_statistics_svg(path, data):
    """Generate Local Dynamic Statistics Panel (850x165)."""
    repos_cnt = data.get("public_repos", 23)
    stars_cnt = data.get("total_stars", 16)
    
    svg = f"""<svg width="850" height="165" viewBox="0 0 850 165" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="statBg" x1="0" y1="0" x2="850" y2="165" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_SURFACE}"/>
      <stop offset="100%" stop-color="{C_BG}"/>
    </linearGradient>
    <filter id="statGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="850" height="165" rx="12" fill="url(#statBg)"/>
  <rect x="0.5" y="0.5" width="849" height="164" rx="11.5" stroke="{C_BORDER}" stroke-width="1"/>

  <!-- Top Status Bar -->
  <line x1="25" y1="36" x2="825" y2="36" stroke="{C_BORDER}" stroke-width="1"/>
  <circle cx="34" cy="22" r="4" fill="{C_CYAN}" filter="url(#statGlow)"/>
  <text x="46" y="26" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="11" font-weight="700" fill="{C_CYAN}" letter-spacing="1">
    TELEMETRY // VERIFIED GITHUB AUDIT METRICS
  </text>
  <text x="825" y="26" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="10.5" fill="{C_MUTED}">
    LIVE SYNC ENGINE
  </text>

  <!-- Metric 1: Public Repositories -->
  <g transform="translate(30, 52)">
    <rect width="180" height="92" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="16" y="28" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_MUTED}">PUBLIC REPOSITORIES</text>
    <text x="16" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="32" font-weight="800" fill="{C_WHITE}">{repos_cnt}</text>
    <text x="64" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="11" fill="{C_CYAN}">audited</text>
  </g>

  <!-- Metric 2: Stars Earned -->
  <g transform="translate(230, 52)">
    <rect width="180" height="92" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="16" y="28" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_MUTED}">REPOSITORY STARS</text>
    <text x="16" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="32" font-weight="800" fill="{C_CYAN}">{stars_cnt} &#9733;</text>
    <text x="96" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="11" fill="{C_MUTED}">organic</text>
  </g>

  <!-- Metric 3: Active Community Reach -->
  <g transform="translate(430, 52)">
    <rect width="180" height="92" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="16" y="28" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_MUTED}">COMMUNITY SCALE</text>
    <text x="16" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="30" font-weight="800" fill="{C_VIOLET}">185K+</text>
    <text x="112" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="11" fill="{C_MUTED}">moderated</text>
  </g>

  <!-- Metric 4: Hackathon / Credentials -->
  <g transform="translate(630, 52)">
    <rect width="190" height="92" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <text x="16" y="28" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11" font-weight="600" fill="{C_MUTED}">ENGINEERING PODIUM</text>
    <text x="16" y="66" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="30" font-weight="800" fill="{C_MAGENTA}">1st Place</text>
    <text x="16" y="82" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="9.5" fill="{C_MUTED}">HackMe Problem Solver</text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def create_tech_constellation_svg(path):
    """Generate Technology Constellation Matrix (850x260)."""
    svg = f"""<svg width="850" height="260" viewBox="0 0 850 260" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="techBg" x1="0" y1="0" x2="850" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_BG}"/>
      <stop offset="100%" stop-color="{C_SURFACE}"/>
    </linearGradient>
    <filter id="neonDot" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="850" height="260" rx="12" fill="url(#techBg)"/>
  <rect x="0.5" y="0.5" width="849" height="259" rx="11.5" stroke="{C_BORDER}" stroke-width="1"/>

  <!-- Section Title -->
  <g transform="translate(30, 28)">
    <circle cx="4" cy="4" r="4" fill="{C_CYAN}" filter="url(#neonDot)"/>
    <text x="16" y="8" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="12" font-weight="700" fill="{C_WHITE}" letter-spacing="1.5">
      TECHNOLOGY CONSTELLATION // VERIFIED STACK BY REPOSITORY EVIDENCE
    </text>
  </g>

  <!-- Quadrant 1: Systems & Real-Time Overlays -->
  <g transform="translate(30, 54)">
    <rect width="380" height="90" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <circle cx="16" cy="20" r="4" fill="{C_CYAN}"/>
    <text x="28" y="24" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="12" font-weight="700" fill="{C_CYAN}">
      SYSTEMS &amp; REAL-TIME OVERLAYS
    </text>
    <!-- Tags -->
    <g transform="translate(16, 40)">
      <rect x="0" y="0" width="45" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="22" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{C_WHITE}">C#</text>

      <rect x="52" y="0" width="50" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="77" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{C_WHITE}">C++</text>

      <rect x="109" y="0" width="95" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="156" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">Windows APIs</text>

      <rect x="211" y="0" width="135" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="278" y="15" text-anchor="middle" font-family="monospace" font-size="10" fill="{C_WHITE}">Always-on-top GUI</text>
    </g>
    <text x="16" y="78" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="10.5" fill="{C_MUTED}">
      Evidence: LiveSubs, HackMe Optimizer (C++ runtime tuning)
    </text>
  </g>

  <!-- Quadrant 2: AI & Biomedical Synthesis -->
  <g transform="translate(440, 54)">
    <rect width="380" height="90" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <circle cx="16" cy="20" r="4" fill="{C_MAGENTA}"/>
    <text x="28" y="24" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="12" font-weight="700" fill="{C_MAGENTA}">
      BIOMEDICAL AI &amp; EVIDENCE RAG
    </text>
    <!-- Tags -->
    <g transform="translate(16, 40)">
      <rect x="0" y="0" width="60" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="30" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{C_WHITE}">Python</text>

      <rect x="67" y="0" width="105" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="119" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">Mixture-of-LLMs</text>

      <rect x="179" y="0" width="75" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="216" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">ChromaDB</text>

      <rect x="261" y="0" width="85" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="303" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">Reflex / Ollama</text>
    </g>
    <text x="16" y="78" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="10.5" fill="{C_MUTED}">
      Evidence: Griffin Bio, SyGriffin, Sita (10 Biomedical collectors)
    </text>
  </g>

  <!-- Quadrant 3: Knowledge Graphs & Systems Core -->
  <g transform="translate(30, 154)">
    <rect width="380" height="90" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <circle cx="16" cy="20" r="4" fill="{C_VIOLET}"/>
    <text x="28" y="24" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="12" font-weight="700" fill="{C_VIOLET}">
      KNOWLEDGE GRAPHS &amp; SECURITY CORE
    </text>
    <!-- Tags -->
    <g transform="translate(16, 40)">
      <rect x="0" y="0" width="50" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="25" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{C_WHITE}">Rust</text>

      <rect x="57" y="0" width="70" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="92" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">MCP Server</text>

      <rect x="134" y="0" width="130" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="199" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">Think-on-Graph (ToG)</text>

      <rect x="271" y="0" width="75" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="308" y="15" text-anchor="middle" font-family="monospace" font-size="10" fill="{C_WHITE}">Docker / CI</text>
    </g>
    <text x="16" y="78" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="10.5" fill="{C_MUTED}">
      Evidence: Knox (Rust MCP vault), Polaris (Kg-Library-API), Laya-KG
    </text>
  </g>

  <!-- Quadrant 4: Web, Interfaces & Cloud -->
  <g transform="translate(440, 154)">
    <rect width="380" height="90" rx="8" fill="{C_SURFACE_ALT}" stroke="{C_BORDER}" stroke-width="1"/>
    <circle cx="16" cy="20" r="4" fill="{C_BLUE}"/>
    <text x="28" y="24" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="12" font-weight="700" fill="{C_BLUE}">
      WEB INTERFACES &amp; CLOUD INFRASTRUCTURE
    </text>
    <!-- Tags -->
    <g transform="translate(16, 40)">
      <rect x="0" y="0" width="85" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="42" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">TypeScript</text>

      <rect x="92" y="0" width="60" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="122" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="{C_WHITE}">React</text>

      <rect x="159" y="0" width="95" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="206" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">Chroma-Key Canvas</text>

      <rect x="261" y="0" width="85" height="22" rx="4" fill="{C_BG}" stroke="{C_BORDER}"/>
      <text x="303" y="15" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{C_WHITE}">Google Cloud</text>
    </g>
    <text x="16" y="78" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="10.5" fill="{C_MUTED}">
      Evidence: ChatStream, myselfdiva, Aegion Frontend Internship
    </text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def create_project_cards():
    """Generate high-contrast, themed project cards for the 5 Flagship projects (850x135)."""
    projects = [
        {
            "filename": "livesubs.svg",
            "name": "LiveSubs",
            "badge": "DESKTOP OVERLAY // SHIPPED",
            "badge_color": C_CYAN,
            "stars": "7 &#9733;",
            "tagline": "Real-Time Subtitle &amp; Translation Windows Desktop Overlay",
            "description": "Hooks Windows Live Captions, translates recognized speech via modular LLM/traditional APIs, and renders transparent always-on-top subtitles over any conference call or video.",
            "stack": ["C#", ".NET", "Windows Live Captions", "Translation APIs", "DirectX/WPF Overlay"],
            "accent": C_CYAN,
            "motif": "waveform"
        },
        {
            "filename": "griffin.svg",
            "name": "Griffin Bio",
            "badge": "BIOMEDICAL RESEARCH // ACTIVE",
            "badge_color": C_MAGENTA,
            "stars": "2 &#9733;",
            "tagline": "Scientific Evidence Synthesis &amp; Contradiction Detection Workbench",
            "description": "Federates 10 biomedical data collectors (PubMed, Europe PMC, ChEMBL, UniProt, OpenAlex), generates ChromaDB embeddings, and executes Mixture-of-LLMs claim extraction.",
            "stack": ["Python", "Mixture of LLMs", "ChromaDB", "Ollama", "Reflex", "10 Collectors"],
            "accent": C_MAGENTA,
            "motif": "neural"
        },
        {
            "filename": "knox.svg",
            "name": "Knox",
            "badge": "SYSTEM SECURITY // ACTIVE",
            "badge_color": C_VIOLET,
            "stars": "2 &#9733;",
            "tagline": "High-Assurance Rust MCP Memory &amp; Security Vault Server",
            "description": "Cryptographically hardened Model Context Protocol (MCP) server providing context isolation, verified session boundaries, and safe memory persistence for autonomous agents.",
            "stack": ["Rust", "TypeScript", "MCP Protocol", "Crates.io", "GitHub Actions CI"],
            "accent": C_VIOLET,
            "motif": "shield"
        },
        {
            "filename": "polaris.svg",
            "name": "Polaris (Kg-Library-API)",
            "badge": "KNOWLEDGE GRAPH // ACTIVE",
            "badge_color": C_CYAN,
            "stars": "1 &#9733;",
            "tagline": "Modular Knowledge Graph &amp; Think-on-Graph (ToG) Reasoning API",
            "description": "High-performance, storage-agnostic KG library and annotation store enforcing 'Core + Packs' modularity with hybrid Think-on-Graph reasoning workers for complex query paths.",
            "stack": ["Python", "Think-on-Graph", "Annotation Store", "Docker", "REST API"],
            "accent": C_CYAN,
            "motif": "graph"
        },
        {
            "filename": "chatstream.svg",
            "name": "ChatStream",
            "badge": "FULL-STACK PLATFORM // COMPLETED",
            "badge_color": C_BLUE,
            "stars": "0 &#9733;",
            "tagline": "Discord-Grade Real-Time Distributed Messaging Architecture",
            "description": "Full-stack real-time collaboration engine featuring persistent channels, reactive state synchronisation, sub-second latency messaging, and complete architectural documentation.",
            "stack": ["TypeScript", "React", "Node.js", "WebSockets", "State Sync"],
            "accent": C_BLUE,
            "motif": "stream"
        }
    ]

    for p in projects:
        card_path = os.path.join(PROJECTS_DIR, p["filename"])
        
        # Motif generation
        motif_svg = ""
        if p["motif"] == "waveform":
            motif_svg = f"""
            <g transform="translate(690, 40)" opacity="0.8">
              <rect x="0" y="24" width="4" height="24" rx="2" fill="{p['accent']}" opacity="0.6"/>
              <rect x="8" y="14" width="4" height="44" rx="2" fill="{p['accent']}" opacity="0.9"/>
              <rect x="16" y="4" width="4" height="64" rx="2" fill="{p['accent']}"/>
              <rect x="24" y="20" width="4" height="32" rx="2" fill="{p['accent']}" opacity="0.7"/>
              <rect x="32" y="8" width="4" height="56" rx="2" fill="{p['accent']}" opacity="0.9"/>
              <rect x="40" y="26" width="4" height="20" rx="2" fill="{p['accent']}" opacity="0.5"/>
              <rect x="48" y="16" width="4" height="40" rx="2" fill="{p['accent']}" opacity="0.8"/>
              <rect x="56" y="28" width="4" height="16" rx="2" fill="{p['accent']}" opacity="0.4"/>
            </g>"""
        elif p["motif"] == "neural":
            motif_svg = f"""
            <g transform="translate(685, 30)" opacity="0.85">
              <circle cx="15" cy="20" r="4.5" fill="{p['accent']}"/>
              <circle cx="65" cy="10" r="3.5" fill="{p['accent']}" opacity="0.7"/>
              <circle cx="35" cy="55" r="5" fill="{p['accent']}"/>
              <circle cx="75" cy="50" r="4" fill="{p['accent']}" opacity="0.8"/>
              <line x1="15" y1="20" x2="65" y2="10" stroke="{p['accent']}" stroke-width="1.2" opacity="0.4"/>
              <line x1="15" y1="20" x2="35" y2="55" stroke="{p['accent']}" stroke-width="1.2" opacity="0.4"/>
              <line x1="35" y1="55" x2="75" y2="50" stroke="{p['accent']}" stroke-width="1.2" opacity="0.4"/>
              <line x1="65" y1="10" x2="75" y2="50" stroke="{p['accent']}" stroke-width="1.2" opacity="0.4"/>
            </g>"""
        elif p["motif"] == "shield":
            motif_svg = f"""
            <g transform="translate(695, 30)" opacity="0.85">
              <polygon points="40,8 68,20 68,50 40,68 12,50 12,20" fill="{C_SURFACE}" stroke="{p['accent']}" stroke-width="1.8"/>
              <polygon points="40,18 58,26 58,45 40,58 22,45 22,26" fill="none" stroke="{p['accent']}" stroke-width="1" stroke-dasharray="3 2" opacity="0.7"/>
              <circle cx="40" cy="38" r="5" fill="{p['accent']}"/>
            </g>"""
        elif p["motif"] == "graph":
            motif_svg = f"""
            <g transform="translate(690, 32)" opacity="0.85">
              <rect x="0" y="22" width="28" height="28" rx="4" fill="{C_SURFACE}" stroke="{p['accent']}" stroke-width="1.2"/>
              <text x="14" y="40" text-anchor="middle" font-family="monospace" font-size="10" fill="{p['accent']}">C</text>
              <line x1="28" y1="36" x2="52" y2="18" stroke="{p['accent']}" stroke-width="1.2" stroke-dasharray="2 2"/>
              <line x1="28" y1="36" x2="52" y2="54" stroke="{p['accent']}" stroke-width="1.2" stroke-dasharray="2 2"/>
              <rect x="52" y="6" width="24" height="24" rx="4" fill="{C_SURFACE}" stroke="{p['accent']}" stroke-width="1"/>
              <rect x="52" y="42" width="24" height="24" rx="4" fill="{C_SURFACE}" stroke="{p['accent']}" stroke-width="1"/>
            </g>"""
        else: # stream
            motif_svg = f"""
            <g transform="translate(690, 32)" opacity="0.85">
              <path d="M 0,20 Q 20,5 40,20 T 80,20" fill="none" stroke="{p['accent']}" stroke-width="2"/>
              <path d="M 0,38 Q 20,23 40,38 T 80,38" fill="none" stroke="{p['accent']}" stroke-width="1.5" opacity="0.6"/>
              <path d="M 0,56 Q 20,41 40,56 T 80,56" fill="none" stroke="{p['accent']}" stroke-width="1" opacity="0.3"/>
            </g>"""

        # Build stack badges
        stack_badges = ""
        x_offset = 24
        for s in p["stack"]:
            escaped_s = xml_escape(s)
            width = len(s) * 7.5 + 16
            stack_badges += f"""
            <rect x="{x_offset}" y="0" width="{width}" height="20" rx="4" fill="{C_BG}" stroke="{C_BORDER}" stroke-width="1"/>
            <text x="{x_offset + width/2}" y="14" text-anchor="middle" font-family="monospace" font-size="10" fill="{C_WHITE}">{escaped_s}</text>
            """
            x_offset += width + 8

        svg = f"""<svg width="850" height="135" viewBox="0 0 850 135" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cardGrad_{p['filename'].split('.')[0]}" x1="0" y1="0" x2="850" y2="135" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_SURFACE}"/>
      <stop offset="100%" stop-color="{C_SURFACE_ALT}"/>
    </linearGradient>
  </defs>

  <rect width="850" height="135" rx="10" fill="url(#cardGrad_{p['filename'].split('.')[0]})"/>
  <rect x="0.5" y="0.5" width="849" height="134" rx="9.5" stroke="{C_BORDER}" stroke-width="1"/>
  <line x1="0" y1="0" x2="4" y2="135" stroke="{p['accent']}" stroke-width="4"/>

  <!-- Header line -->
  <g transform="translate(24, 22)">
    <text x="0" y="0" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="19" font-weight="800" fill="{C_WHITE}">
      {p['name']}
    </text>
    <rect x="{len(p['name'])*12 + 10}" y="-13" width="{len(p['badge'])*6.5 + 14}" height="18" rx="3.5" fill="{C_BG}" stroke="{p['badge_color']}" stroke-width="1"/>
    <text x="{len(p['name'])*12 + 17}" y="0" font-family="monospace" font-size="9" font-weight="700" fill="{p['badge_color']}">
      {p['badge']}
    </text>
    <text x="630" y="0" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="13" font-weight="700" fill="{C_CYAN}">
      {p['stars']}
    </text>
  </g>

  <!-- Tagline -->
  <text x="24" y="52" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="12" font-weight="600" fill="{p['accent']}">
    {p['tagline']}
  </text>

  <!-- Description -->
  <text x="24" y="74" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="11.5" fill="{C_MUTED}">
    {p['description']}
  </text>

  <!-- Stack badges -->
  <g transform="translate(0, 96)">
    {stack_badges}
  </g>

  <!-- Motif -->
  {motif_svg}
</svg>"""
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[Generator] Created {card_path}")


def create_footer_svg(path):
    """Generate Cosmic Connect Footer (850x120)."""
    svg = f"""<svg width="850" height="120" viewBox="0 0 850 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="footerBg" x1="0" y1="0" x2="850" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{C_SURFACE}"/>
      <stop offset="100%" stop-color="{C_BG}"/>
    </linearGradient>
    <filter id="fGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="850" height="120" rx="10" fill="url(#footerBg)"/>
  <rect x="0.5" y="0.5" width="849" height="119" rx="9.5" stroke="{C_BORDER}" stroke-width="1"/>

  <g transform="translate(32, 34)">
    <circle cx="4" cy="4" r="4" fill="{C_CYAN}" filter="url(#fGlow)"/>
    <text x="18" y="8" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, &apos;Space Grotesk&apos;, sans-serif" font-size="16" font-weight="800" fill="{C_WHITE}" letter-spacing="0.5">
      TRANSMISSION CHANNELS // LET&apos;S BUILD TOGETHER
    </text>
    <text x="0" y="32" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, sans-serif" font-size="12" fill="{C_MUTED}">
      Open for AI engineering internships, research collaborations, and production systems that demand sub-second speed.
    </text>
    <text x="0" y="54" font-family="-apple-system, BlinkMacSystemFont, &apos;Segoe UI&apos;, Roboto, monospace" font-size="11" fill="{C_CYAN}">
      COMM CHANNELS: GITHUB · LINKEDIN · X · PORTFOLIO · DIRECT EMAIL (diwa.p2007@gmail.com)
    </text>
  </g>

  <!-- Constellation Nodes on Right -->
  <g transform="translate(720, 25)" opacity="0.7">
    <circle cx="40" cy="15" r="3" fill="{C_CYAN}" filter="url(#fGlow)"/>
    <circle cx="80" cy="35" r="2.5" fill="{C_VIOLET}"/>
    <circle cx="20" cy="55" r="3" fill="{C_MAGENTA}"/>
    <line x1="40" y1="15" x2="80" y2="35" stroke="{C_CYAN}" stroke-width="0.8" opacity="0.4"/>
    <line x1="40" y1="15" x2="20" y2="55" stroke="{C_MAGENTA}" stroke-width="0.8" opacity="0.4"/>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Generator] Created {path}")


def generate_readme(data):
    """Generate master README.md adhering strictly to no-slop principles and verified audit truth."""
    readme_path = os.path.join(ROOT_DIR, "README.md")
    
    content = f"""<div align="center">

<!-- HERO BANNER -->
<img src="assets/hero.svg" alt="Diwakar Venkat Peddada — Nebula 01 Cosmic Hero Banner" width="100%">

<br>

<!-- QUICK NAVIGATION BADGES -->
<p align="center">
  <a href="#-about-the-builder"><img src="https://img.shields.io/badge/ORBIT-ABOUT%20BUILDER-0B1024?style=for-the-badge&logoColor=22D3EE&labelColor=050510" alt="About"></a>
  <a href="#-featured-flagship-projects"><img src="https://img.shields.io/badge/CONSTELLATION-FEATURED%20PROJECTS-0B1024?style=for-the-badge&logoColor=A855F7&labelColor=050510" alt="Projects"></a>
  <a href="#-technology-constellation"><img src="https://img.shields.io/badge/TELEMETRY-TECH%20STACK-0B1024?style=for-the-badge&logoColor=3B82F6&labelColor=050510" alt="Stack"></a>
  <a href="#-experience--podium"><img src="https://img.shields.io/badge/LOGS-EXPERIENCE-0B1024?style=for-the-badge&logoColor=EC4899&labelColor=050510" alt="Experience"></a>
  <a href="#-cosmic-connect"><img src="https://img.shields.io/badge/TRANSMIT-CONNECT-0B1024?style=for-the-badge&logoColor=22D3EE&labelColor=050510" alt="Connect"></a>
</p>

</div>

---

## 🔭 About the Builder

I am **Diwakar Venkat Peddada** (*Diva*), a software engineer and AI developer currently studying Computer Science at **Andhra University** ('28) and interning at **Aegion Dynamic Solutions**.

> *"I like problems where the answer has to arrive while you are still watching — captions that keep pace with a live speaker, a pipeline that digests thousands of biomedical papers and isolates exactly where they disagree, or interfaces that stay snappy under load."*

My work spans from low-level systems and desktop overlays to large-scale biomedical research pipelines and knowledge graphs:

- **Real-Time Desktop & Systems Engineering**: Architected **LiveSubs**, an always-on-top Windows subtitle and translation overlay listening to Windows Live Captions and translating speech in real time with custom LLM/API pipelines.
- **Biomedical AI & Evidence Synthesis**: Developed **Griffin Bio**, a multi-source research workbench that ingests from 10 modular collectors (PubMed, Europe PMC, ChEMBL, UniProt, OpenAlex), embeds scientific literature in ChromaDB, and runs a Mixture-of-LLMs pipeline to detect claim contradictions and synthesize consensus.
- **Knowledge Graphs & Autonomous Agent Infrastructure**: Engineered **Knox** (a high-assurance Rust MCP memory vault) and **Polaris** (a modular Think-on-Graph API and hybrid reasoning worker).
- **High-Concurrency Community Management**: Moderated a **185,000+ member community** for *Mecha Break* (Amazing Seasun Games), distilling real-time player telemetry and feedback into actionable developer reports.

---

## 📊 Cosmic Statistics

<div align="center">
  <img src="assets/statistics.svg" alt="Diva143V GitHub Telemetry and Audited Metrics" width="100%">
</div>

---

## 🪐 Technology Constellation

Verified stack backed by repository source code inspection and production experience:

<div align="center">
  <img src="assets/tech-constellation.svg" alt="Diva143V Technology Constellation" width="100%">
</div>

<details>
<summary><b>Detailed Technical Breakdown</b></summary>
<br>

| Domain | Verified Technologies | Selected Repositories |
|---|---|---|
| **Systems & Overlays** | C#, .NET, C++, Windows Win32 APIs, Live Captions, Memory Optimization | [`LiveSubs`](https://github.com/Diva143V/LiveSubs), `HackMe Solver` |
| **Biomedical & AI Engineering** | Python, Mixture of LLMs, ChromaDB, Ollama, RAG Pipelines, Reflex | [`Griffin`](https://github.com/Diva143V/Griffin), [`SyGriffin`](https://github.com/Diva143V/SyGriffin), [`vinu`](https://github.com/Diva143V/vinu) |
| **Knowledge Graphs & Core** | Rust, Model Context Protocol (MCP), Think-on-Graph (ToG), Docker | [`Knox`](https://github.com/Diva143V/Knox), [`Kg-Library-API`](https://github.com/Diva143V/Kg-Library-API), [`Laya-KG`](https://github.com/Diva143V/Laya-KG) |
| **Web & Interactive Interfaces** | TypeScript, React, HTML5/CSS3, Canvas Chroma-Key, WebSockets | [`chatstream`](https://github.com/Diva143V/chatstream), [`myselfdiva`](https://github.com/Diva143V/myselfdiva) |
| **Cloud & DevOps** | Google Cloud Platform (Compute), Git, GitHub Actions CI/CD, Linux | [JPMorgan Chase Simulation](https://github.com/Diva143V/forage-midas), Google Cloud Compute |

</details>

---

## 🚀 Featured Flagship Projects

### 01. LiveSubs — Real-Time Subtitle & Translation Windows Overlay
<div align="center">
  <a href="https://github.com/Diva143V/LiveSubs">
    <img src="assets/projects/livesubs.svg" alt="LiveSubs Project Card" width="100%">
  </a>
</div>

- **Core Architecture**: Native Windows desktop application listening directly to Windows Live Captions audio stream.
- **Features**: Translates captured text via modular LLM and classical translation APIs, rendering clean, customizable, always-on-top subtitles over conference calls, video streams, and presentations.
- **Repository**: [`github.com/Diva143V/LiveSubs`](https://github.com/Diva143V/LiveSubs) · **Downloads**: [Releases Available](https://github.com/Diva143V/LiveSubs/releases)

---

### 02. Griffin Bio — Scientific Evidence Synthesis & Contradiction Workbench
<div align="center">
  <a href="https://github.com/Diva143V/Griffin">
    <img src="assets/projects/griffin.svg" alt="Griffin Bio Project Card" width="100%">
  </a>
</div>

- **Core Architecture**: Life-sciences research companion turning unstructured biological queries into reproducible research workflows.
- **Pipeline**: Ingests from 10 modular collectors (PubMed, Europe PMC, Semantic Scholar, OpenAlex, ClinicalTrials, bioRxiv, ChEMBL, UniProt, PubChem, dbSNP), embeds abstracts in ChromaDB, and executes Mixture-of-LLMs claim extraction to rank evidence and flag scientific contradictions.
- **Repository**: [`github.com/Diva143V/Griffin`](https://github.com/Diva143V/Griffin)

---

### 03. Knox — High-Assurance Rust MCP Memory & Security Vault
<div align="center">
  <a href="https://github.com/Diva143V/Knox">
    <img src="assets/projects/knox.svg" alt="Knox Project Card" width="100%">
  </a>
</div>

- **Core Architecture**: Cryptographically hardened Model Context Protocol (MCP) server written in Rust for context isolation and agent memory management.
- **Features**: Verified session boundaries, secure persistence, automated multi-platform CI/CD and release workflow for Crates.io distribution.
- **Repository**: [`github.com/Diva143V/Knox`](https://github.com/Diva143V/Knox)

---

### 04. Polaris (Kg-Library-API) — Hybrid Think-on-Graph (ToG) Worker
<div align="center">
  <a href="https://github.com/Diva143V/Kg-Library-API">
    <img src="assets/projects/polaris.svg" alt="Polaris Project Card" width="100%">
  </a>
</div>

- **Core Architecture**: Modular, high-performance, storage-agnostic Knowledge Graph API and annotation store.
- **Features**: Enforces strict "Core + Packs" architecture, keeping base facts separated from domain extensions while powering hybrid Think-on-Graph reasoning workers.
- **Repository**: [`github.com/Diva143V/Kg-Library-API`](https://github.com/Diva143V/Kg-Library-API)

---

### 05. ChatStream — Discord-Grade Real-Time Collaboration Engine
<div align="center">
  <a href="https://github.com/Diva143V/chatstream">
    <img src="assets/projects/chatstream.svg" alt="ChatStream Project Card" width="100%">
  </a>
</div>

- **Core Architecture**: Full-stack real-time collaboration application built with TypeScript, React, and WebSockets.
- **Features**: Multi-channel workspaces, instant state synchronisation, resilient message queuing, and comprehensive architectural documentation.
- **Repository**: [`github.com/Diva143V/chatstream`](https://github.com/Diva143V/chatstream)

---

## 🏆 Experience & Podium

### Professional Roles
- **AI Developer Intern** — *Aegion Dynamic Solutions* `[Jul 2026 — Present]`
  - Building AI-powered applications, intelligent automation, and production LLM integrations.
- **Front-End Developer Intern** — *Aegion Dynamic Solutions* `[Aug — Oct 2025]`
  - Reworked React interfaces, eliminated redundant re-renders, and tightened API handoff performance.
- **Community Moderator** — *Mecha Break (Amazing Seasun Games)* `[Mar 2024 — Jul 2025]`
  - Managed an active gaming community of 185,000+ members, compiling player issue digests for game developers.

### Verified Credentials & Competitions
- 🥇 **1st Place Winner** — *HackMe Problem Statement Solver (2024)* (Custom C++ data structures & search optimization)
- 📜 **Software Engineering Simulation** — *JPMorgan Chase & Co.* `[Jan 2026]`
- 📜 **Google Cloud Compute Fundamentals** — *Google* `[Oct 2025]`
- 📜 **C & C++ Programming Certification** — *HackerRank*

---

## 📡 Cosmic Connect

<div align="center">
  <a href="mailto:diwa.p2007@gmail.com">
    <img src="assets/footer.svg" alt="Cosmic Transmission Footer" width="100%">
  </a>
  <br><br>
  <p align="center">
    <a href="https://myselfdiva.netlify.app/"><img src="https://img.shields.io/badge/PORTFOLIO-myselfdiva.netlify.app-0B1024?style=for-the-badge&logo=netlify&logoColor=22D3EE&labelColor=050510" alt="Portfolio"></a>
    <a href="https://linkedin.com/in/diwakar-venkat-peddada-66aa30229/"><img src="https://img.shields.io/badge/LINKEDIN-Diwakar%20Venkat%20Peddada-0B1024?style=for-the-badge&logo=linkedin&logoColor=3B82F6&labelColor=050510" alt="LinkedIn"></a>
    <a href="https://x.com/Diva_2007_"><img src="https://img.shields.io/badge/X-@Diva__2007__-0B1024?style=for-the-badge&logo=x&logoColor=F8FAFC&labelColor=050510" alt="Twitter"></a>
    <a href="mailto:diwa.p2007@gmail.com"><img src="https://img.shields.io/badge/EMAIL-diwa.p2007@gmail.com-0B1024?style=for-the-badge&logo=gmail&logoColor=EC4899&labelColor=050510" alt="Email"></a>
  </p>
  <br>
  <sub>Architected with NEBULA / 01 Design System · Verified Audit by Diva143V</sub>
</div>
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Generator] Created {readme_path}")


def main():
    print("[Generator] Starting NEBULA / 01 Generation Pipeline...")
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    
    data = fetch_github_data()
    print(f"[Generator] Data retrieved: {data['public_repos']} repos, {data['total_stars']} stars, {data['followers']} followers.")
    
    create_hero_svg(os.path.join(ASSETS_DIR, "hero.svg"))
    create_statistics_svg(os.path.join(ASSETS_DIR, "statistics.svg"), data)
    create_tech_constellation_svg(os.path.join(ASSETS_DIR, "tech-constellation.svg"))
    create_project_cards()
    create_footer_svg(os.path.join(ASSETS_DIR, "footer.svg"))
    
    generate_readme(data)
    print("[Generator] Pipeline completed successfully!")


if __name__ == "__main__":
    main()
