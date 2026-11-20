"""SVG artwork for the solar-system profile.

The drawings are generated rather than hand-edited so the README can be rebuilt
from one source and checked in CI. Everything here is deterministic: same
content, same bytes.
"""

from __future__ import annotations

import base64
import html
import math
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# Palette
BG = "#04070F"
PANEL = "#080D18"
SURFACE = "#0C1424"
BORDER = "#1B2A44"
INK = "#F4F7FC"
MUTED = "#93A1B6"
FAINT = "#5E6E85"
GOLD = "#FFB020"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"
MONO = "ui-monospace, 'Cascadia Mono', 'SFMono-Regular', Consolas, monospace"

STARS = (
    (32, 34, 1.2, 0.55, "a"),
    (94, 88, 0.8, 0.35, ""),
    (148, 42, 1.0, 0.45, "b"),
    (206, 112, 0.7, 0.3, ""),
    (260, 28, 1.1, 0.5, "c"),
    (318, 74, 0.8, 0.35, ""),
    (378, 38, 0.9, 0.4, ""),
    (424, 132, 0.7, 0.25, ""),
    (466, 58, 1.2, 0.55, "b"),
    (520, 24, 0.8, 0.35, ""),
    (566, 96, 0.7, 0.3, ""),
    (612, 40, 1.0, 0.45, "a"),
    (708, 34, 0.8, 0.3, ""),
    (762, 104, 1.1, 0.45, "c"),
    (822, 42, 0.9, 0.4, ""),
    (846, 154, 0.7, 0.25, ""),
    (812, 214, 1.0, 0.35, ""),
    (842, 330, 0.8, 0.3, "b"),
    (802, 420, 1.1, 0.45, ""),
    (742, 474, 0.7, 0.25, ""),
    (668, 492, 0.9, 0.35, "c"),
    (602, 470, 0.7, 0.25, ""),
    (520, 498, 1.0, 0.4, ""),
    (420, 484, 0.8, 0.3, ""),
    (320, 500, 1.1, 0.4, "a"),
    (238, 470, 0.7, 0.25, ""),
    (146, 492, 0.9, 0.35, ""),
    (72, 450, 1.0, 0.4, "b"),
    (28, 382, 0.7, 0.25, ""),
    (56, 304, 1.1, 0.4, ""),
    (26, 222, 0.8, 0.3, "c"),
    (44, 142, 0.9, 0.35, ""),
    (118, 168, 0.7, 0.25, ""),
    (192, 214, 0.8, 0.3, ""),
    (252, 176, 0.6, 0.2, ""),
    (344, 168, 0.7, 0.25, ""),
    (392, 236, 0.6, 0.2, ""),
    (318, 320, 0.7, 0.25, ""),
    (196, 372, 0.6, 0.2, ""),
    (438, 398, 0.7, 0.25, ""),
    (548, 364, 0.6, 0.2, ""),
    (688, 388, 0.7, 0.25, ""),
    (746, 320, 0.6, 0.2, ""),
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: float = 12,
    fill: str = INK,
    family: str = SANS,
    weight: int = 400,
    spacing: float | None = None,
    anchor: str | None = None,
    element_id: str | None = None,
) -> str:
    attrs = [
        f'x="{x:g}"',
        f'y="{y:g}"',
        f'font-family="{family}"',
        f'font-size="{size:g}"',
        f'font-weight="{weight}"',
        f'fill="{fill}"',
    ]
    if element_id:
        attrs.append(f'id="{element_id}"')
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing:g}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    return f'<text {" ".join(attrs)}>{esc(value)}</text>'


def svg(w: int, h: int, title: str, desc: str, body: str) -> str:
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" '
        'xmlns="http://www.w3.org/2000/svg" role="img" '
        'aria-labelledby="title desc">\n'
        f'  <title id="title">{esc(title)}</title>\n'
        f'  <desc id="desc">{esc(desc)}</desc>\n'
        f"{body}\n"
        "</svg>\n"
    )


def _avatar_data_uri() -> str:
    # The 240px JPEG keeps the two SVG copies small. If someone replaces the
    # source avatar, they should replace this JPEG with a fresh 240px export.
    jpg = ASSETS / "avatar-240.jpg"
    png = ASSETS / "avatar.png"
    path = jpg if jpg.is_file() else png
    mime = "image/jpeg" if path.suffix.lower() == ".jpg" else "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _stars() -> str:
    parts = []
    for x, y, r, opacity, twinkle in STARS:
        cls = f' class="twinkle-{twinkle}"' if twinkle else ""
        parts.append(
            f'  <circle cx="{x}" cy="{y}" r="{r:g}" fill="{INK}" '
            f'opacity="{opacity:g}"{cls}/>'
        )
    return "\n".join(parts)


def _hero_avatars(avatar: str) -> str:
    return f"""  <g transform="translate(662 258)">
    <circle r="82" fill="url(#sunGlow)" class="breathe"/>
    <circle r="54" fill="url(#sunGlow)" opacity=".8"/>
    <circle r="47" fill="#050810"/>
    <g clip-path="url(#sunClip)">
      <image href="{avatar}" x="-44" y="-44" width="88" height="88" preserveAspectRatio="xMidYMid slice"/>
      <circle r="44" fill="url(#sunShade)"/>
    </g>
    <circle r="46" fill="none" stroke="{GOLD}" stroke-width="2"/>
    <circle r="51" fill="none" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1" stroke-dasharray="3 7"/>
  </g>"""


def _planet(p: content.Planet, cx: float = 662, cy: float = 258) -> str:
    angle = math.radians(p.angle)
    x = cx + p.radius * math.cos(angle)
    y = cy + p.radius * math.sin(angle)
    body = max(7, p.radius / 15)
    moons = ""
    if p.moons:
        moon_orbit = body + 8
        for index in range(p.moons):
            moon_angle = math.radians(-58 + index * 118)
            mx = moon_orbit * math.cos(moon_angle)
            my = moon_orbit * math.sin(moon_angle)
            moons += (
                f'\n    <circle cx="{mx:.1f}" cy="{my:.1f}" r="1.5" '
                f'fill="{INK}" opacity=".8"/>'
            )
        moons = (
            f'\n    <circle r="{moon_orbit:.1f}" fill="none" stroke="{p.color}" '
            f'stroke-opacity=".25" stroke-width=".7" stroke-dasharray="1.5 3"/>'
            + moons
        )
    return f"""  <g class="planet" transform="translate({x:.1f} {y:.1f})">
    <circle r="{p.radius / 8 + 6:.1f}" fill="{p.color}" opacity=".10"/>
    <circle r="{body:.1f}" fill="{p.color}"/>
    <circle r="{body:.1f}" fill="url(#sphere)"/>
    <circle r="{body:.1f}" fill="none" stroke="{p.color}" stroke-opacity=".65"/>{moons}
  </g>"""


def build_hero() -> str:
    avatar = _avatar_data_uri()
    orbits = "\n".join(
        f'  <circle class="orbit" r="{p.radius}" stroke="{BORDER}" stroke-width="1" '
        f'stroke-dasharray="2 7"/>'
        for p in content.PLANETS
    )
    planets = "\n".join(_planet(p) for p in content.PLANETS)
    body = f"""  <defs>
    <radialGradient id="space" cx="50%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#0B1830"/>
      <stop offset="48%" stop-color="#060C18"/>
      <stop offset="100%" stop-color="{BG}"/>
    </radialGradient>
    <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{GOLD}" stop-opacity=".55"/>
      <stop offset="42%" stop-color="#FF7A3D" stop-opacity=".24"/>
      <stop offset="100%" stop-color="#FF7A3D" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sunShade" cx="34%" cy="28%" r="76%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity=".18"/>
      <stop offset="52%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity=".55"/>
    </radialGradient>
    <radialGradient id="sphere" cx="34%" cy="28%" r="76%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity=".48"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity=".58"/>
    </radialGradient>
    <linearGradient id="cometTail" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{GOLD}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{GOLD}" stop-opacity=".8"/>
    </linearGradient>
    <clipPath id="sunClip"><circle r="44"/></clipPath>
    <style>
      .rise {{ animation: rise 900ms cubic-bezier(.2,.7,.2,1) both; }}
      .d1 {{ animation-delay: 80ms; }}
      .d2 {{ animation-delay: 170ms; }}
      .d3 {{ animation-delay: 260ms; }}
      .fade {{ animation: fade 1100ms ease-out 350ms both; }}
      .breathe {{ animation: breathe 6s ease-in-out infinite; }}
      .comet {{ animation: comet 22s linear 4s infinite both; }}
      .twinkle-a {{ animation: twinkle 4.5s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 6s ease-in-out 1.2s infinite; }}
      .twinkle-c {{ animation: twinkle 7.5s ease-in-out 2.4s infinite; }}
      @keyframes rise {{
        from {{ transform: translateY(12px); }}
        to {{ transform: translateY(0); }}
      }}
      @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
      @keyframes breathe {{
        0%, 100% {{ opacity: .62; }}
        50% {{ opacity: .9; }}
      }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: .22; }}
        50% {{ opacity: .85; }}
      }}
      @keyframes comet {{
        0% {{ opacity: 0; transform: translate(-80px, 390px); }}
        8% {{ opacity: .7; }}
        88% {{ opacity: .7; }}
        100% {{ opacity: 0; transform: translate(920px, 40px); }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .rise, .fade, .breathe, .comet, .twinkle-a, .twinkle-b, .twinkle-c {{
          animation: none !important;
        }}
        .rise, .fade {{ opacity: 1; transform: none; }}
        .comet {{ display: none; }}
      }}
    </style>
  </defs>

  <rect width="880" height="520" rx="16" fill="url(#space)"/>
  <rect x=".5" y=".5" width="879" height="519" rx="15.5" stroke="{BORDER}"/>
  <g class="fade">
{_stars()}
  </g>

  <g class="rise d1">
    <circle cx="49" cy="41" r="4" fill="{GOLD}"/>
    {text(63, 46, "SOLAR SYSTEM // DIVA143V", size=11, fill=GOLD, family=MONO, weight=700, spacing=1.7)}
  </g>
  <g class="rise d1">
    {text(836, 46, "PLANETS = LANGUAGES / MOONS = PROJECTS", size=9, fill=FAINT, family=MONO, spacing=.4, anchor="end")}
  </g>
  <line class="fade" x1="48" y1="72" x2="832" y2="72" stroke="{BORDER}"/>

  <g class="rise d1">
    {text(48, 160, "DIWAKAR", size=64, weight=800, spacing=-2, element_id="name-1")}
  </g>
  <g class="rise d2">
    {text(48, 220, "VENKAT", size=64, weight=800, spacing=-2, element_id="name-2")}
  </g>
  <g class="rise d3">
    {text(48, 280, "PEDDADA", size=64, weight=800, spacing=-2, fill=GOLD, element_id="name-3")}
  </g>

  <g class="rise d2">
    {text(48, 342, content.HERO_TAGLINE[0], size=17, fill=MUTED, element_id="tagline-1")}
    {text(48, 366, content.HERO_TAGLINE[1], size=17, fill=MUTED, element_id="tagline-2")}
  </g>
  <line class="fade" x1="48" y1="394" x2="112" y2="394" stroke="{GOLD}" stroke-width="2"/>
  <g class="rise d3">
    {text(48, 424, "AI developer / Visakhapatnam, India", size=11.5, fill=FAINT, family=MONO, spacing=.4)}
  </g>

  <g class="fade" transform="translate(662 258)">
{orbits}
  </g>
{_hero_avatars(avatar)}
{planets}

  <g class="comet">
    <line x1="-62" y1="0" x2="0" y2="0" stroke="url(#cometTail)" stroke-width="1.6" stroke-linecap="round"/>
    <circle r="2" fill="{INK}"/>
  </g>
"""
    return svg(880, 520, content.HERO_ALT, content.HERO_DESC, body)


def _pill(x: float, y: float, label: str, color: str) -> tuple[str, float]:
    width = max(78, len(label) * 6.2 + 24)
    body = (
        f'<rect x="{x:g}" y="{y:g}" width="{width:.1f}" height="23" rx="4" '
        f'fill="{SURFACE}" stroke="{BORDER}"/>\n'
        + text(
            x + width / 2,
            y + 15,
            label,
            size=9.5,
            fill=color,
            family=MONO,
            weight=700,
            anchor="middle",
            spacing=.3,
        )
    )
    return body, width


def build_about() -> str:
    avatar = _avatar_data_uri()
    pills = []
    x = 170.0
    for label, color in content.FACTS:
        markup, width = _pill(x, 170, label, color)
        pills.append(markup)
        x += width + 10
    body = f"""  <defs>
    <radialGradient id="aboutGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{GOLD}" stop-opacity=".55"/>
      <stop offset="58%" stop-color="#FF7A3D" stop-opacity=".18"/>
      <stop offset="100%" stop-color="#FF7A3D" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aboutShade" cx="34%" cy="28%" r="76%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity=".16"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity=".5"/>
    </radialGradient>
    <clipPath id="aboutClip"><circle r="46"/></clipPath>
    <style>
      .breathe {{ animation: breathe 6s ease-in-out infinite; }}
      @keyframes breathe {{ 0%, 100% {{ opacity: .65; }} 50% {{ opacity: .95; }} }}
      @media (prefers-reduced-motion: reduce) {{ .breathe {{ animation: none; }} }}
    </style>
  </defs>

  <rect width="880" height="214" rx="14" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="879" height="213" rx="13.5" stroke="{BORDER}"/>

  <g transform="translate(88 105)">
    <circle r="62" fill="url(#aboutGlow)" class="breathe"/>
    <circle r="48" fill="#050810"/>
    <g clip-path="url(#aboutClip)">
      <image href="{avatar}" x="-46" y="-46" width="92" height="92" preserveAspectRatio="xMidYMid slice"/>
      <circle r="46" fill="url(#aboutShade)"/>
    </g>
    <circle r="48" fill="none" stroke="{GOLD}" stroke-width="2"/>
  </g>

  <g>
    <circle cx="172" cy="38" r="3" fill="{GOLD}"/>
    {text(182, 42, "THE SUN // ABOUT", size=10, fill=GOLD, family=MONO, weight=700, spacing=1.4)}
    {text(170, 84, content.NAME, size=28, weight=800, spacing=-.4)}
    {text(170, 108, "Software engineer / AI developer / CS '28 Andhra University", size=12, fill=MUTED, family=MONO)}
    {text(170, 134, content.ABOUT_QUOTE[0], size=12.5, fill=MUTED)}
    {text(170, 152, content.ABOUT_QUOTE[1], size=12.5, fill=MUTED)}
  </g>
  <g>
    {"".join(pills)}
  </g>
"""
    return svg(
        880,
        214,
        f"About {content.NAME}",
        "A short introduction with Diwakar's role, community work, competition win and location.",
        body,
    )


def _tags(tags: tuple[str, ...], accent: str) -> str:
    parts = []
    x = 20.0
    for tag in tags:
        width = max(38, len(tag) * 6.2 + 12)
        parts.append(
            f'<rect x="{x:.1f}" y="0" width="{width:.1f}" height="19" rx="3" '
            f'fill="{SURFACE}" stroke="{BORDER}"/>'
            + text(
                x + width / 2,
                13,
                tag,
                size=8.5,
                fill=INK,
                family=MONO,
                anchor="middle",
            )
        )
        x += width + 6
    return "\n      ".join(parts)


def build_card(project: content.Project) -> str:
    body = f"""  <rect width="430" height="168" rx="11" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="429" height="167" rx="10.5" stroke="{BORDER}"/>
  <rect width="3.5" height="168" rx="1.75" fill="{project.accent}"/>

  <g transform="translate(20 27)">
    {text(0, 0, project.moon, size=8.5, fill=project.accent, family=MONO, weight=700, spacing=.6)}
    {text(388, 0, "↗", size=14, fill=FAINT, anchor="end")}
  </g>
  {text(20, 56, project.name, size=19, weight=800)}
  {text(20, 77, project.subtitle, size=11.5, weight=600)}
  {text(20, 98, project.body[0], size=9.5, fill=MUTED)}
  {text(20, 113, project.body[1], size=9.5, fill=MUTED)}

  <g transform="translate(0 133)">
      {_tags(project.tags, project.accent)}
  </g>
"""
    return svg(
        430,
        168,
        f"{project.name}: {project.role}",
        project.alt,
        body,
    )


def build_stack() -> str:
    rows = []
    for index, planet in enumerate(content.PLANETS):
        y = 62 + index * 31
        rows.append(
            f"""  <g>
    <circle cx="34" cy="{y - 4}" r="4.5" fill="{planet.color}"/>
    {text(48, y, planet.name, size=12.5, weight=700)}
    {text(168, y, planet.orbit, size=9.5, fill=planet.color, family=MONO)}
    <line x1="260" y1="{y - 4}" x2="292" y2="{y - 4}" stroke="{planet.color}" stroke-opacity=".7" stroke-width="1.5"/>
    <circle cx="292" cy="{y - 4}" r="2" fill="{planet.color}"/>
    {text(306, y, planet.domain, size=10, fill=MUTED)}
    {text(654, y, planet.evidence, size=9.5, fill=planet.color, family=MONO)}
  </g>"""
        )
    body = f"""  <rect width="880" height="226" rx="14" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="879" height="225" rx="13.5" stroke="{BORDER}"/>

  <g transform="translate(28 29)">
    <circle cx="5" cy="5" r="4" fill="{GOLD}"/>
    {text(18, 9, "THE PLANETS // LANGUAGES & ORBITS", size=10, fill=GOLD, family=MONO, weight=700, spacing=1.2)}
  </g>
  <line x1="28" y1="44" x2="852" y2="44" stroke="{BORDER}"/>

{chr(10).join(rows)}

  {text(28, 214, "Orbit order is a reading order, not a ranking.", size=9, fill=FAINT, family=MONO)}
"""
    return svg(
        880,
        226,
        "Languages and orbits",
        "Five languages, the kind of work each one supports, and the projects that use them.",
        body,
    )


def _stat_box(x: int, label: str, big: str, small: str, color: str, big_size: int = 25) -> str:
    return f"""  <g transform="translate({x} 48)">
    <rect width="195" height="80" rx="7" fill="{SURFACE}" stroke="{BORDER}"/>
    {text(16, 23, label, size=9, fill=MUTED, family=MONO, spacing=.7)}
    {text(16, 57, big, size=big_size, fill=color, weight=800, spacing=-.4)}
    {text(16, 73, small, size=9.5, fill=MUTED, family=MONO)}
  </g>"""


def build_log() -> str:
    body = f"""  <rect width="880" height="148" rx="14" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="879" height="147" rx="13.5" stroke="{BORDER}"/>

  <g transform="translate(28 29)">
    <circle cx="5" cy="5" r="4" fill="{GOLD}"/>
    {text(18, 9, "SOLAR LOG // CURRENT ORBIT", size=10, fill=GOLD, family=MONO, weight=700, spacing=1.2)}
  </g>
  <line x1="28" y1="42" x2="852" y2="42" stroke="{BORDER}"/>

{_stat_box(28, "CURRENT ORBIT", "AI INTERN", "Aegion Dynamic", "#4CC9F0")}
{_stat_box(238, "COMMUNITY", "185K+", "Mecha Break", "#C084FC", 28)}
{_stat_box(448, "PODIUM", "1ST PLACE", "HackMe 2024", "#F472B6", 23)}
{_stat_box(658, "BASED IN", "Visakhapatnam", "India / UTC+05:30", "#FB923C", 18)}
"""
    return svg(
        880,
        148,
        "Current orbit and record",
        "AI developer intern at Aegion Dynamic Solutions, 185,000-person community moderator, first place at HackMe 2024, based in Visakhapatnam.",
        body,
    )


def build_footer() -> str:
    body = f"""  <rect width="880" height="86" rx="12" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="879" height="85" rx="11.5" stroke="{BORDER}"/>

  <circle cx="44" cy="43" r="17" fill="{SURFACE}" stroke="{GOLD}"/>
  <circle cx="44" cy="43" r="6" fill="{GOLD}"/>
  {text(76, 38, "Let's build something that has to keep up.", size=15.5, weight=800)}
  {text(76, 58, f"{content.EMAIL} / {content.LOCATION} / UTC+05:30", size=10, fill=MUTED, family=MONO)}

  <g transform="translate(715 28)">
    <rect width="137" height="30" rx="4" fill="{SURFACE}" stroke="{GOLD}"/>
    {text(68.5, 19, "EMAIL →", size=9.5, fill=GOLD, family=MONO, weight=700, anchor="middle", spacing=.8)}
  </g>
"""
    return svg(
        880,
        86,
        "Email Diwakar",
        f"Write to {content.EMAIL}.",
        body,
    )
