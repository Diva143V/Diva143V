#!/usr/bin/env python3
"""
NEBULA // SOLAR SYSTEM — GitSkins-Adapted Engine for Diva143V
Generates the complete interactive Solar System GitHub Profile README, SVGs, and assets.
"""

import os
import xml.etree.ElementTree as ET

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
CARDS_DIR = os.path.join(ASSETS_DIR, "solar-cards")
README_PATH = os.path.join(ROOT_DIR, "README.md")

# Palette Tokens (Solar System Deep Space)
C_SPACE = "#05070F"
C_PANEL = "#080C1A"
C_SURFACE = "#0B1024"
C_BORDER = "#1E293B"
C_SUN_CORE = "#FFA726"
C_SUN_GLOW = "#FF7043"
C_WHITE = "#F8FAFC"
C_MUTED = "#94A3B8"
C_FAINT = "#475569"

# Planet Colors
C_PYTHON = "#38BDF8"      # Cyan / Light Blue
C_CSHARP = "#C084FC"      # Electric Violet / Purple
C_RUST = "#FB923C"        # Rust Amber / Orange
C_TYPESCRIPT = "#60A5FA"  # Royal Cosmic Blue
C_CPP = "#F472B6"         # Neon Magenta / Pink


def create_solar_orbits_svg(path):
    """
    Generate the centerpiece Solar System SVG (880x520).
    Features:
    - Glowing central Sun representing Diva143V
    - 5 concentric Keplerian elliptical orbits
    - 5 language planets (Python, C#, Rust, TypeScript, C++) with SMIL animateMotion
    - Moons representing flagship projects (Griffin Bio, SyGriffin, LiveSubs, Knox, ChatStream, HackMe)
    - Comets representing recent pushes/activity
    """
    cx, cy = 440, 260
    
    orbits = [
        {
            "name": "Python",
            "color": C_PYTHON,
            "rx": 135,
            "ry": 65,
            "r": 13,
            "dur": "18s",
            "moons": [
                {"name": "Griffin Bio", "dist": 22, "r": 3.5, "dur": "4s", "color": C_WHITE},
                {"name": "SyGriffin", "dist": 34, "r": 3.0, "dur": "6.5s", "color": "#F472B6"}
            ]
        },
        {
            "name": "C#",
            "color": C_CSHARP,
            "rx": 190,
            "ry": 95,
            "r": 12,
            "dur": "29s",
            "moons": [
                {"name": "LiveSubs (7★)", "dist": 24, "r": 4.0, "dur": "4.5s", "color": C_WHITE}
            ]
        },
        {
            "name": "Rust",
            "color": C_RUST,
            "rx": 245,
            "ry": 125,
            "r": 11,
            "dur": "42s",
            "moons": [
                {"name": "Knox (2★)", "dist": 22, "r": 3.5, "dur": "5s", "color": C_WHITE}
            ]
        },
        {
            "name": "TypeScript",
            "color": C_TYPESCRIPT,
            "rx": 300,
            "ry": 155,
            "r": 10,
            "dur": "56s",
            "moons": [
                {"name": "ChatStream", "dist": 20, "r": 3.0, "dur": "5.5s", "color": C_WHITE}
            ]
        },
        {
            "name": "C++",
            "color": C_CPP,
            "rx": 355,
            "ry": 185,
            "r": 9.5,
            "dur": "72s",
            "moons": [
                {"name": "HackMe (1st)", "dist": 19, "r": 3.0, "dur": "6s", "color": C_WHITE}
            ]
        }
    ]

    star_coords = [
        (45, 35, 1.2, 0.8), (110, 80, 0.8, 0.4), (180, 40, 1.0, 0.6), (270, 75, 0.7, 0.3),
        (350, 30, 1.1, 0.7), (430, 60, 0.9, 0.5), (510, 25, 1.4, 0.9), (600, 70, 0.8, 0.4),
        (690, 45, 1.2, 0.8), (770, 30, 0.7, 0.3), (840, 85, 1.0, 0.6), (820, 160, 0.8, 0.4),
        (850, 250, 1.1, 0.7), (830, 340, 0.9, 0.5), (860, 440, 1.3, 0.8), (780, 480, 0.7, 0.3),
        (700, 460, 1.0, 0.6), (620, 490, 0.8, 0.4), (530, 475, 1.2, 0.7), (440, 500, 0.9, 0.5),
        (350, 470, 1.1, 0.8), (260, 495, 0.7, 0.3), (170, 460, 1.0, 0.6), (90, 485, 0.8, 0.4),
        (30, 440, 1.2, 0.7), (50, 350, 0.7, 0.3), (25, 260, 1.0, 0.6), (40, 170, 0.9, 0.5),
        (130, 150, 0.6, 0.25), (200, 190, 0.5, 0.2), (680, 180, 0.6, 0.3), (740, 220, 0.5, 0.2),
        (160, 340, 0.6, 0.25), (220, 380, 0.5, 0.2), (660, 350, 0.6, 0.3), (720, 390, 0.5, 0.2),
        (380, 120, 0.7, 0.3), (500, 130, 0.6, 0.25), (370, 400, 0.7, 0.3), (510, 390, 0.6, 0.25)
    ]
    stars_svg = "\n".join([
        f'    <circle cx="{x}" cy="{y}" r="{r}" fill="#F8FAFC" opacity="{op}"/>'
        for x, y, r, op in star_coords
    ])

    orbits_svg = ""
    for idx, orb in enumerate(orbits):
        rx, ry = orb["rx"], orb["ry"]
        dur = orb["dur"]
        color = orb["color"]
        pr = orb["r"]
        name = orb["name"]
        
        path_d = f"M {cx - rx},{cy} a {rx},{ry} 0 1,0 {2*rx},0 a {rx},{ry} 0 1,0 {-2*rx},0"
        
        orbits_svg += f"""
    <!-- Orbit {idx+1}: {name} -->
    <path id="orbit_{idx}" d="{path_d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1" stroke-dasharray="3 6"/>
        """

        moons_svg = ""
        for m_idx, moon in enumerate(orb["moons"]):
            m_name = moon["name"]
            m_dist = moon["dist"]
            m_r = moon["r"]
            m_dur = moon["dur"]
            m_color = moon["color"]
            moons_svg += f"""
        <g>
          <animateTransform attributeName="transform" type="rotate" from="{m_idx*180}" to="{m_idx*180 + 360}" dur="{m_dur}" repeatCount="indefinite"/>
          <circle cx="{m_dist}" cy="0" r="{m_r}" fill="{m_color}"/>
          <text x="{m_dist + 5}" y="3" font-family="ui-monospace, monospace" font-size="7.5" font-weight="600" fill="#E2E8F0" opacity="0.85">{m_name}</text>
        </g>"""

        orbits_svg += f"""
    <g>
      <animateMotion path="{path_d}" dur="{dur}" repeatCount="indefinite"/>
      <circle cx="0" cy="0" r="{pr}" fill="{color}" filter="url(#planetShade)"/>
      <circle cx="0" cy="0" r="{pr + 2}" fill="none" stroke="{color}" stroke-opacity="0.35" stroke-width="1"/>
      <text x="0" y="{-pr - 4}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="9" font-weight="700" fill="#F8FAFC">{name}</text>
      {moons_svg}
    </g>
        """

    svg = f"""<svg width="880" height="520" viewBox="0 0 880 520" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="spaceGlow" cx="440" cy="260" r="420" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0E162E"/>
      <stop offset="60%" stop-color="#080C1A"/>
      <stop offset="100%" stop-color="{C_SPACE}"/>
    </radialGradient>

    <radialGradient id="sunCorona" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{C_SUN_CORE}" stop-opacity="0.8"/>
      <stop offset="45%" stop-color="{C_SUN_GLOW}" stop-opacity="0.35"/>
      <stop offset="80%" stop-color="{C_SUN_GLOW}" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="{C_SPACE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sunCoreGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFF7ED"/>
      <stop offset="30%" stop-color="{C_SUN_CORE}"/>
      <stop offset="100%" stop-color="{C_SUN_GLOW}"/>
    </radialGradient>

    <radialGradient id="planetShade" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.5"/>
      <stop offset="40%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.6"/>
    </radialGradient>

    <linearGradient id="cometTail" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0"/>
      <stop offset="85%" stop-color="#38BDF8" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.95"/>
    </linearGradient>
    <linearGradient id="cometTail2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#EC4899" stop-opacity="0"/>
      <stop offset="85%" stop-color="#EC4899" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.9"/>
    </linearGradient>

    <filter id="sunBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect width="880" height="520" rx="14" fill="url(#spaceGlow)"/>
  <rect x="0.5" y="0.5" width="879" height="519" rx="13.5" stroke="{C_BORDER}" stroke-width="1"/>

  <g id="starfield">
{stars_svg}
  </g>

  <g id="planetary_system">
{orbits_svg}
  </g>

  <!-- Central Sun (Diwakar / Diva143V) -->
  <g id="the_sun" transform="translate({cx}, {cy})">
    <circle cx="0" cy="0" r="64" fill="url(#sunCorona)">
      <animate attributeName="r" values="64;74;64" dur="4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.8;1;0.8" dur="4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="48" fill="url(#sunCorona)" opacity="0.6"/>
    <circle cx="0" cy="0" r="32" fill="url(#sunCoreGrad)" stroke="#FFA726" stroke-width="1.5" filter="url(#sunBlur)"/>
    <circle cx="0" cy="0" r="32" fill="url(#sunCoreGrad)" stroke="#FFA726" stroke-width="1.5"/>

    <text x="0" y="-6" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" font-weight="700" fill="#7C2D12" letter-spacing="1">THE SUN</text>
    <text x="0" y="10" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="13" font-weight="900" fill="#431407">DIVA</text>
    <text x="0" y="44" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="10.5" font-weight="700" fill="#F8FAFC">Diwakar Venkat Peddada</text>
    <text x="0" y="57" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" fill="{C_MUTED}">17.68° N · 83.22° E</text>
  </g>

  <!-- Comet 1 -->
  <g>
    <animateMotion path="M -120,40 L 1000,240" dur="13s" repeatCount="indefinite"/>
    <line x1="-50" y1="0" x2="0" y2="0" stroke="url(#cometTail)" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="3" fill="#FFFFFF"/>
    <text x="-60" y="-6" font-family="ui-monospace, monospace" font-size="7.5" fill="#38BDF8">commit push</text>
  </g>

  <!-- Comet 2 -->
  <g>
    <animateMotion path="M -100,420 L 980,180" dur="18s" repeatCount="indefinite"/>
    <line x1="-40" y1="0" x2="0" y2="0" stroke="url(#cometTail2)" stroke-width="2" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="2.5" fill="#FFFFFF"/>
    <text x="-50" y="-5" font-family="ui-monospace, monospace" font-size="7" fill="#F472B6">telemetry</text>
  </g>

  <!-- Legend -->
  <g transform="translate(28, 26)">
    <rect width="180" height="22" rx="4" fill="{C_PANEL}" fill-opacity="0.85" stroke="{C_BORDER}" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="{C_SUN_CORE}"/>
    <text x="22" y="15" font-family="ui-monospace, monospace" font-size="9" font-weight="600" fill="{C_SUN_CORE}" letter-spacing="0.5">SOLAR SYSTEM ENGINE</text>
  </g>
  <g transform="translate(640, 26)">
    <rect width="212" height="22" rx="4" fill="{C_PANEL}" fill-opacity="0.85" stroke="{C_BORDER}" stroke-width="0.8"/>
    <text x="106" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" fill="{C_MUTED}">planets = lang · moons = repos</text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Solar Generator] Created {path}")


def create_solar_about_svg(path):
    """Generate The Sun / About Card (880x190)."""
    svg = f"""<svg width="880" height="190" viewBox="0 0 880 190" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="aboutSunCorona" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{C_SUN_CORE}" stop-opacity="0.7"/>
      <stop offset="60%" stop-color="{C_SUN_GLOW}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{C_SPACE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aboutSunCore" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFF7ED"/>
      <stop offset="30%" stop-color="{C_SUN_CORE}"/>
      <stop offset="100%" stop-color="{C_SUN_GLOW}"/>
    </radialGradient>
  </defs>

  <rect width="880" height="190" rx="12" fill="{C_PANEL}"/>
  <rect x="0.5" y="0.5" width="879" height="189" rx="11.5" stroke="{C_BORDER}" stroke-width="1"/>

  <g transform="translate(85, 95)">
    <circle cx="0" cy="0" r="54" fill="url(#aboutSunCorona)">
      <animate attributeName="r" values="54;60;54" dur="4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="0" cy="0" r="34" fill="url(#aboutSunCore)" stroke="#FFA726" stroke-width="1.5"/>
    <text x="0" y="-5" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8" font-weight="700" fill="#7C2D12">THE SUN</text>
    <text x="0" y="11" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="14" font-weight="900" fill="#431407">DIVA</text>
  </g>

  <g transform="translate(170, 32)">
    <rect width="130" height="20" rx="3" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
    <circle cx="10" cy="10" r="2.5" fill="{C_SUN_CORE}"/>
    <text x="20" y="14" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="{C_SUN_CORE}" letter-spacing="0.8">CENTRAL STAR</text>

    <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="24" font-weight="800" fill="{C_WHITE}">Diwakar Venkat Peddada</text>
    <text x="0" y="66" font-family="ui-monospace, monospace" font-size="12" font-weight="500" fill="{C_MUTED}">Software Engineer · AI Developer · CS &apos;28 Andhra University</text>

    <text x="0" y="94" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="{C_MUTED}">
      &quot;I like problems where the answer has to arrive while you are still watching — captions that keep pace
    </text>
    <text x="0" y="112" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12.5" fill="{C_MUTED}">
      with a live speaker, a pipeline that reads thousands of biomedical papers, and interfaces that stay quick under load.&quot;
    </text>

    <g transform="translate(0, 126)">
      <rect width="165" height="22" rx="4" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
      <text x="82" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="{C_PYTHON}">AI INTERN @ AEGION</text>

      <rect x="175" width="160" height="22" rx="4" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
      <text x="255" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="{C_CSHARP}">185K COMMUNITY MOD</text>

      <rect x="345" width="150" height="22" rx="4" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
      <text x="420" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="{C_CPP}">1ST PLACE HACKME</text>

      <rect x="505" width="165" height="22" rx="4" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
      <text x="587" y="15" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9" fill="{C_RUST}">VISAKHAPATNAM, IN</text>
    </g>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Solar Generator] Created {path}")


def create_solar_cards():
    """Generate 4 Moon project cards (430x150) for a 2x2 grid in README."""
    cards = [
        {
            "filename": "card-livesubs.svg",
            "moon_badge": "MOON 01 // C# ORBIT",
            "badge_color": C_CSHARP,
            "title": "LiveSubs",
            "stars": "7 &#9733;",
            "tagline": "Real-time subtitle &amp; translation Windows overlay.",
            "desc": "Listens to Live Captions, translates via LLM or classic APIs, renders always-on-top transparent subtitles.",
            "techs": ["C#", ".NET", "Live Captions", "Translation", "WPF Overlay"],
            "accent": C_CSHARP
        },
        {
            "filename": "card-griffin.svg",
            "moon_badge": "MOON 02 // PYTHON ORBIT",
            "badge_color": C_PYTHON,
            "title": "Griffin Bio",
            "stars": "2 &#9733;",
            "tagline": "Scientific evidence synthesis &amp; contradiction workbench.",
            "desc": "Ingests from 10 biomedical source collectors, embeds in ChromaDB, runs Mixture-of-LLMs claim extraction.",
            "techs": ["Python", "ChromaDB RAG", "Ollama", "Reflex", "10 Collectors"],
            "accent": C_PYTHON
        },
        {
            "filename": "card-knox.svg",
            "moon_badge": "MOON 03 // RUST ORBIT",
            "badge_color": C_RUST,
            "title": "Knox",
            "stars": "2 &#9733;",
            "tagline": "Rust Model Context Protocol (MCP) memory vault.",
            "desc": "Session isolation, verified boundaries, secure persistence for AI agents. Crates.io releases with CI/CD.",
            "techs": ["Rust", "TypeScript", "MCP Protocol", "Crates.io", "CI/CD"],
            "accent": C_RUST
        },
        {
            "filename": "card-sygriffin.svg",
            "moon_badge": "MOON 04 // BIOINFORMATICS",
            "badge_color": C_CPP,
            "title": "SyGriffin",
            "stars": "2 &#9733;",
            "tagline": "CLI-first AI bioinformatics platform for neoantigens.",
            "desc": "Analyzes tumor VCF files, predicts vaccine-relevant peptide candidates with transparent scoring &amp; reports.",
            "techs": ["Python", "R", "TypeScript", "Neoantigen", "VCF Pipeline"],
            "accent": C_CPP
        }
    ]

    for c in cards:
        card_path = os.path.join(CARDS_DIR, c["filename"])
        
        tags_svg = ""
        x_off = 20
        for t in c["techs"]:
            w = len(t) * 6.5 + 14
            tags_svg += f"""
      <rect x="{x_off}" y="0" width="{w}" height="18" rx="3" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
      <text x="{x_off + w/2}" y="12.5" text-anchor="middle" font-family="ui-monospace, monospace" font-size="8.5" fill="{C_WHITE}">{t}</text>
            """
            x_off += w + 6

        svg = f"""<svg width="430" height="150" viewBox="0 0 430 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="430" height="150" rx="10" fill="{C_PANEL}"/>
  <rect x="0.5" y="0.5" width="429" height="149" rx="9.5" stroke="{C_BORDER}" stroke-width="1"/>
  <rect width="3.5" height="150" fill="{c['accent']}" rx="0"/>

  <g transform="translate(20, 24)">
    <text x="0" y="0" font-family="ui-monospace, monospace" font-size="8.5" font-weight="700" fill="{c['badge_color']}" letter-spacing="0.5">{c['moon_badge']}</text>
    <text x="390" y="0" text-anchor="end" font-family="ui-monospace, monospace" font-size="10.5" font-weight="700" fill="{c['accent']}">{c['stars']}</text>
  </g>

  <text x="20" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="18" font-weight="800" fill="{C_WHITE}">{c['title']}</text>

  <text x="20" y="74" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="11.5" font-weight="600" fill="{C_WHITE}">{c['tagline']}</text>
  <text x="20" y="92" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="10.5" fill="{C_MUTED}">{c['desc']}</text>

  <g transform="translate(0, 114)">
    {tags_svg}
  </g>
</svg>"""
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"[Solar Generator] Created {card_path}")


def create_solar_stack_svg(path):
    """Generate The Planets / Stack Card (880x210)."""
    svg = f"""<svg width="880" height="210" viewBox="0 0 880 210" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="880" height="210" rx="12" fill="{C_PANEL}"/>
  <rect x="0.5" y="0.5" width="879" height="209" rx="11.5" stroke="{C_BORDER}" stroke-width="1"/>

  <g transform="translate(28, 26)">
    <circle cx="5" cy="5" r="4" fill="{C_SUN_CORE}"/>
    <text x="18" y="9" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="{C_SUN_CORE}" letter-spacing="1">THE PLANETARY SYSTEM // PROGRAMMING LANGUAGES &amp; ORBITS</text>
  </g>

  <g transform="translate(28, 50)">
    <circle cx="6" cy="10" r="5" fill="{C_PYTHON}"/>
    <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="{C_WHITE}">Python</text>
    <text x="110" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_PYTHON}">Orbit 1 (Inner)</text>
    <rect x="220" y="4" width="380" height="12" rx="3" fill="{C_SURFACE}"/>
    <rect x="220" y="4" width="280" height="12" rx="3" fill="{C_PYTHON}" fill-opacity="0.8"/>
    <text x="615" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_MUTED}">Biomedical AI · RAG · ChromaDB · Ollama · Reflex</text>
  </g>

  <g transform="translate(28, 80)">
    <circle cx="6" cy="10" r="5" fill="{C_CSHARP}"/>
    <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="{C_WHITE}">C# / .NET</text>
    <text x="110" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_CSHARP}">Orbit 2</text>
    <rect x="220" y="4" width="380" height="12" rx="3" fill="{C_SURFACE}"/>
    <rect x="220" y="4" width="220" height="12" rx="3" fill="{C_CSHARP}" fill-opacity="0.8"/>
    <text x="615" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_MUTED}">Live Captions · Windows Overlays · Speech Translation</text>
  </g>

  <g transform="translate(28, 110)">
    <circle cx="6" cy="10" r="5" fill="{C_RUST}"/>
    <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="{C_WHITE}">Rust</text>
    <text x="110" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_RUST}">Orbit 3</text>
    <rect x="220" y="4" width="380" height="12" rx="3" fill="{C_SURFACE}"/>
    <rect x="220" y="4" width="160" height="12" rx="3" fill="{C_RUST}" fill-opacity="0.8"/>
    <text x="615" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_MUTED}">Model Context Protocol (MCP) · Crates.io · Vaults</text>
  </g>

  <g transform="translate(28, 140)">
    <circle cx="6" cy="10" r="5" fill="{C_TYPESCRIPT}"/>
    <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="{C_WHITE}">TypeScript</text>
    <text x="110" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_TYPESCRIPT}">Orbit 4</text>
    <rect x="220" y="4" width="380" height="12" rx="3" fill="{C_SURFACE}"/>
    <rect x="220" y="4" width="130" height="12" rx="3" fill="{C_TYPESCRIPT}" fill-opacity="0.8"/>
    <text x="615" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_MUTED}">React · WebSockets · Real-Time Collaboration · Node</text>
  </g>

  <g transform="translate(28, 170)">
    <circle cx="6" cy="10" r="5" fill="{C_CPP}"/>
    <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="{C_WHITE}">C++</text>
    <text x="110" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_CPP}">Orbit 5 (Outer)</text>
    <rect x="220" y="4" width="380" height="12" rx="3" fill="{C_SURFACE}"/>
    <rect x="220" y="4" width="100" height="12" rx="3" fill="{C_CPP}" fill-opacity="0.8"/>
    <text x="615" y="14" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_MUTED}">Performance Optimization · Algorithms · Memory Tuning</text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Solar Generator] Created {path}")


def create_solar_log_svg(path):
    """Generate Solar Log / Orbit Telemetry Card (880x140)."""
    svg = f"""<svg width="880" height="140" viewBox="0 0 880 140" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="880" height="140" rx="12" fill="{C_PANEL}"/>
  <rect x="0.5" y="0.5" width="879" height="139" rx="11.5" stroke="{C_BORDER}" stroke-width="1"/>

  <line x1="28" y1="32" x2="852" y2="32" stroke="{C_BORDER}" stroke-width="0.8"/>
  <circle cx="38" cy="18" r="3.5" fill="{C_SUN_CORE}"/>
  <text x="48" y="22" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="{C_SUN_CORE}" letter-spacing="1">SOLAR LOG // ORBIT TELEMETRY &amp; ACHIEVEMENTS</text>

  <g transform="translate(28, 44)">
    <rect width="195" height="78" rx="6" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
    <text x="16" y="24" font-family="ui-monospace, monospace" font-size="9" fill="{C_MUTED}">TOTAL REPOSITORIES</text>
    <text x="16" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="28" font-weight="800" fill="{C_WHITE}">23</text>
    <text x="56" y="56" font-family="ui-monospace, monospace" font-size="10" fill="{C_PYTHON}">public moons</text>
  </g>

  <g transform="translate(238, 44)">
    <rect width="195" height="78" rx="6" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
    <text x="16" y="24" font-family="ui-monospace, monospace" font-size="9" fill="{C_MUTED}">STARS EARNED</text>
    <text x="16" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="28" font-weight="800" fill="{C_SUN_CORE}">16 &#9733;</text>
    <text x="86" y="56" font-family="ui-monospace, monospace" font-size="10" fill="{C_MUTED}">organic</text>
  </g>

  <g transform="translate(448, 44)">
    <rect width="195" height="78" rx="6" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
    <text x="16" y="24" font-family="ui-monospace, monospace" font-size="9" fill="{C_MUTED}">COMMUNITY SCALE</text>
    <text x="16" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="26" font-weight="800" fill="{C_CSHARP}">185K+</text>
    <text x="110" y="56" font-family="ui-monospace, monospace" font-size="9.5" fill="{C_MUTED}">moderated</text>
  </g>

  <g transform="translate(658, 44)">
    <rect width="194" height="78" rx="6" fill="{C_SURFACE}" stroke="{C_BORDER}" stroke-width="0.8"/>
    <text x="16" y="24" font-family="ui-monospace, monospace" font-size="9" fill="{C_MUTED}">COMPETITION PODIUM</text>
    <text x="16" y="56" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="24" font-weight="800" fill="{C_CPP}">1st Place</text>
    <text x="16" y="70" font-family="ui-monospace, monospace" font-size="8.5" fill="{C_MUTED}">HackMe · C++ optimization</text>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Solar Generator] Created {path}")


def create_solar_footer_svg(path):
    """Generate Solar Transmission / Footer (880x90)."""
    svg = f"""<svg width="880" height="90" viewBox="0 0 880 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="880" height="90" rx="10" fill="{C_PANEL}"/>
  <rect x="0.5" y="0.5" width="879" height="89" rx="9.5" stroke="{C_BORDER}" stroke-width="1"/>

  <circle cx="32" cy="24" r="3.5" fill="{C_SUN_CORE}">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="44" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="15" font-weight="800" fill="{C_WHITE}">Solar Transmission // Let&apos;s Build Together</text>
  <text x="32" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif" font-size="12" fill="{C_MUTED}">Open for AI engineering internships, research collaborations, and production systems that demand speed.</text>
  <text x="32" y="74" font-family="ui-monospace, monospace" font-size="10" fill="{C_SUN_CORE}">CHANNELS: GITHUB · LINKEDIN · X · PORTFOLIO · DIRECT EMAIL (diwa.p2007@gmail.com)</text>

  <g transform="translate(820, 45)">
    <circle cx="0" cy="0" r="16" fill="{C_SUN_CORE}" fill-opacity="0.15"/>
    <circle cx="0" cy="0" r="9" fill="{C_SUN_CORE}"/>
  </g>
</svg>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[Solar Generator] Created {path}")


def generate_solar_readme():
    """Assemble master README.md using the GitSkins Solar System architecture."""
    content = """<div align="center">

<!-- SOLAR SYSTEM ORBITS HERO -->
<img src="assets/solar-orbits.svg" alt="Solar System: Languages as planets, projects as moons" width="100%">

<br>
<sub><i>I am the sun; my languages are the planets and my projects their moons.</i></sub>
<br><br>

<!-- THE SUN (ABOUT CARD) -->
<img src="assets/solar-about.svg" alt="The Sun — Diwakar Venkat Peddada" width="100%">

</div>

---

## 🌕 The Moons — Featured Repositories

<table border="0" width="100%">
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/Diva143V/LiveSubs">
        <img src="assets/solar-cards/card-livesubs.svg" alt="LiveSubs" width="100%">
      </a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/Diva143V/Griffin">
        <img src="assets/solar-cards/card-griffin.svg" alt="Griffin Bio" width="100%">
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/Diva143V/Knox">
        <img src="assets/solar-cards/card-knox.svg" alt="Knox" width="100%">
      </a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/Diva143V/SyGriffin">
        <img src="assets/solar-cards/card-sygriffin.svg" alt="SyGriffin" width="100%">
      </a>
    </td>
  </tr>
</table>

---

## 🪐 The Planets — Planetary System & Tech Stack

<div align="center">
<img src="assets/solar-stack.svg" alt="Planetary System — Languages & Tech Stack" width="100%">
</div>

<details>
<summary><b>Orbital Distance & Evidence Index</b></summary>
<br>

| Orbit | Celestial Body | Domain | Verified Repositories |
|---|---|---|---|
| **Orbit 1** | **Python** (Inner) | Biomedical AI & Evidence RAG | [`Griffin`](https://github.com/Diva143V/Griffin), [`SyGriffin`](https://github.com/Diva143V/SyGriffin) |
| **Orbit 2** | **C# / .NET** | Windows Subtitle & Overlay Systems | [`LiveSubs`](https://github.com/Diva143V/LiveSubs) |
| **Orbit 3** | **Rust** | High-Assurance MCP Memory Vault | [`Knox`](https://github.com/Diva143V/Knox) |
| **Orbit 4** | **TypeScript** | Real-Time Collaboration & Interfaces | [`chatstream`](https://github.com/Diva143V/chatstream), [`myselfdiva`](https://github.com/Diva143V/myselfdiva) |
| **Orbit 5** | **C++** (Outer) | Algorithmic Optimization & Systems | `HackMe Solver` (1st Place Winner) |

</details>

---

## 📡 Solar Log — Revolutions & Telemetry

<div align="center">
<img src="assets/solar-log.svg" alt="Solar Log — Telemetry & Credentials" width="100%">
</div>

### Verified Experience & Orbit Logs
- **AI Developer Intern** — *Aegion Dynamic Solutions* `[Jul 2026 — Present]`
  - Building AI-powered automation, intelligent workflows, and production LLM integrations.
- **Front-End Developer Intern** — *Aegion Dynamic Solutions* `[Aug — Oct 2025]`
  - Rebuilt React interfaces, trimmed redundant rendering cycles, and tightened API handoffs.
- **Community Moderator** — *Mecha Break (Amazing Seasun Games)* `[Mar 2024 — Jul 2025]`
  - Managed an active gaming community of 185,000+ members, distilling player feedback into developer reports.

### Podium & Credentials
- 🥇 **1st Place Winner** — *HackMe Problem Statement Solver (2024)* (Custom C++ data structures & search tuning)
- 📜 **Software Engineering Simulation** — *JPMorgan Chase & Co.* `[Jan 2026]`
- 📜 **Google Cloud Compute Fundamentals** — *Google* `[Oct 2025]`
- 📜 **C & C++ Programming Certification** — *HackerRank*

---

## ☀️ Transmission Channels

<div align="center">
<a href="mailto:diwa.p2007@gmail.com">
<img src="assets/solar-footer.svg" alt="Solar Transmission" width="100%">
</a>
<br><br>
<p align="center">
  <a href="https://myselfdiva.netlify.app/"><img src="https://img.shields.io/badge/PORTFOLIO-myselfdiva.netlify.app-FFA726?style=for-the-badge&logo=netlify&logoColor=05070F&labelColor=080C1A" alt="Portfolio"></a>
  <a href="https://linkedin.com/in/diwakar-venkat-peddada-66aa30229/"><img src="https://img.shields.io/badge/LINKEDIN-Diwakar%20Venkat%20Peddada-FFA726?style=for-the-badge&logo=linkedin&logoColor=05070F&labelColor=080C1A" alt="LinkedIn"></a>
  <a href="https://x.com/Diva_2007_"><img src="https://img.shields.io/badge/X-@Diva__2007__-FFA726?style=for-the-badge&logo=x&logoColor=05070F&labelColor=080C1A" alt="Twitter"></a>
  <a href="mailto:diwa.p2007@gmail.com"><img src="https://img.shields.io/badge/EMAIL-diwa.p2007@gmail.com-FFA726?style=for-the-badge&logo=gmail&logoColor=05070F&labelColor=080C1A" alt="Email"></a>
</p>
<br>
<sub>Solar System · planets are languages, moons are projects, comets are recent activity</sub>
</div>
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Solar Generator] Created {README_PATH}")


def main():
    print("[Solar Generator] Starting Solar System generation pipeline...")
    os.makedirs(CARDS_DIR, exist_ok=True)
    
    create_solar_orbits_svg(os.path.join(ASSETS_DIR, "solar-orbits.svg"))
    create_solar_about_svg(os.path.join(ASSETS_DIR, "solar-about.svg"))
    create_solar_cards()
    create_solar_stack_svg(os.path.join(ASSETS_DIR, "solar-stack.svg"))
    create_solar_log_svg(os.path.join(ASSETS_DIR, "solar-log.svg"))
    create_solar_footer_svg(os.path.join(ASSETS_DIR, "solar-footer.svg"))
    
    generate_solar_readme()
    print("[Solar Generator] Solar System pipeline completed successfully!")


if __name__ == "__main__":
    main()
