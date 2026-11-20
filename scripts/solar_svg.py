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
from typing import NamedTuple

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
TRACK = "#2A3F66"
GOLD = "#FFB020"
CYAN = "#38BDF8"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"
MONO = "ui-monospace, 'Cascadia Mono', 'SFMono-Regular', Consolas, monospace"


class Star(NamedTuple):
    x: float
    y: float
    r: float
    opacity: float
    twinkle: str = ""
    color: str = INK


STARS: tuple[Star, ...] = (
    Star(32, 34, 1.2, 0.55, "a"),
    Star(94, 88, 0.8, 0.35, "d"),
    Star(148, 42, 1.0, 0.45, "b"),
    Star(206, 112, 0.7, 0.30, ""),
    Star(260, 28, 1.1, 0.50, "c"),
    Star(318, 74, 0.8, 0.35, "d"),
    Star(378, 38, 0.9, 0.40, "a"),
    Star(424, 132, 0.7, 0.25, ""),
    Star(466, 58, 1.2, 0.55, "b", "#38BDF8"),
    Star(520, 24, 0.8, 0.35, "d"),
    Star(566, 96, 0.7, 0.30, ""),
    Star(612, 40, 1.0, 0.45, "a"),
    Star(708, 34, 0.8, 0.30, "d"),
    Star(762, 104, 1.1, 0.45, "c", "#C084FC"),
    Star(856, 24, 0.9, 0.40, "b"),
    Star(846, 154, 0.7, 0.25, ""),
    Star(812, 214, 1.0, 0.35, "a"),
    Star(842, 330, 0.8, 0.30, "b"),
    Star(802, 420, 1.1, 0.45, "c", "#38BDF8"),
    Star(742, 474, 0.7, 0.25, "d"),
    Star(668, 492, 0.9, 0.35, "c"),
    Star(602, 470, 0.7, 0.25, ""),
    Star(520, 498, 1.0, 0.40, "a"),
    Star(420, 484, 0.8, 0.30, "d"),
    Star(320, 500, 1.1, 0.40, "a", "#FFB020"),
    Star(238, 470, 0.7, 0.25, ""),
    Star(146, 492, 0.9, 0.35, "b"),
    Star(72, 450, 1.0, 0.40, "b"),
    Star(28, 382, 0.7, 0.25, "d"),
    Star(56, 304, 1.1, 0.40, "c"),
    Star(26, 222, 0.8, 0.30, "c"),
    Star(44, 142, 0.9, 0.35, "a"),
    Star(118, 168, 0.7, 0.25, ""),
    Star(192, 214, 0.8, 0.30, "d"),
    Star(252, 176, 0.6, 0.20, ""),
    Star(344, 168, 0.7, 0.25, "b"),
    Star(392, 236, 0.6, 0.20, ""),
    Star(318, 320, 0.7, 0.25, "c"),
    Star(196, 372, 0.6, 0.20, ""),
    Star(438, 398, 0.7, 0.25, "a"),
    Star(548, 364, 0.6, 0.20, ""),
    Star(688, 388, 0.7, 0.25, "d"),
    Star(746, 320, 0.6, 0.20, ""),
)

# Extra subtle drifting background dust layer for parallax feel in the hero
DUST_STARS: tuple[tuple[int, int, float, float], ...] = (
    (68, 118, 0.6, 0.22),
    (174, 72, 0.55, 0.20),
    (288, 134, 0.65, 0.24),
    (402, 86, 0.6, 0.22),
    (496, 156, 0.55, 0.18),
    (584, 72, 0.65, 0.24),
    (734, 66, 0.6, 0.22),
    (832, 268, 0.6, 0.22),
    (778, 368, 0.65, 0.24),
    (636, 444, 0.55, 0.20),
    (478, 456, 0.6, 0.22),
    (284, 442, 0.55, 0.20),
    (112, 412, 0.65, 0.24),
    (86, 258, 0.55, 0.18),
)

# Four-point sparkle glints on accent sky coordinates
GLINT_STARS: tuple[tuple[int, int, str, str], ...] = (
    (466, 58, "#38BDF8", "twinkle-b"),
    (762, 104, "#C084FC", "twinkle-c"),
    (802, 420, "#38BDF8", "twinkle-a"),
    (320, 500, "#FFB020", "twinkle-d"),
)

# Kepler-inspired orbital periods (seconds): inner orbits faster, outer slower
PLANET_PERIODS = (18, 28, 40, 54, 72)
MOON_PERIODS = (5.5, 7.5, 9.0, 11.0, 13.0)


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
    for s in STARS:
        cls = f' class="twinkle-{s.twinkle}"' if s.twinkle else ""
        parts.append(
            f'    <circle cx="{s.x:g}" cy="{s.y:g}" r="{s.r:g}" fill="{s.color}" '
            f'opacity="{s.opacity:g}"{cls}/>'
        )
    for gx, gy, color, cls in GLINT_STARS:
        parts.append(
            f'    <g class="{cls}" opacity="0.65">'
            f'<line x1="{gx - 4}" y1="{gy}" x2="{gx + 4}" y2="{gy}" stroke="{color}" stroke-width="0.7" stroke-linecap="round"/>'
            f'<line x1="{gx}" y1="{gy - 4}" x2="{gx}" y2="{gy + 4}" stroke="{color}" stroke-width="0.7" stroke-linecap="round"/>'
            "</g>"
        )
    return "\n".join(parts)


def _dust_stars() -> str:
    return "\n".join(
        f'    <circle cx="{x}" cy="{y}" r="{r:g}" fill="{INK}" opacity="{op:g}"/>'
        for x, y, r, op in DUST_STARS
    )


def _micro_stars(coords: tuple[tuple[int, int, float, str], ...]) -> str:
    return "\n".join(
        f'    <circle cx="{x}" cy="{y}" r="{r:g}" fill="{INK}" opacity="0.35" class="twinkle-{cls}"/>'
        for x, y, r, cls in coords
    )


def _meteor_defs() -> str:
    return f"""    <!-- Shooting star tail gradients (bright head, extra long tail) -->
    <linearGradient id="meteorTailGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{GOLD}" stop-opacity="0" />
      <stop offset="25%" stop-color="{GOLD}" stop-opacity="0.30" />
      <stop offset="65%" stop-color="#FFD166" stop-opacity="0.75" />
      <stop offset="90%" stop-color="#FFF3D6" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="1" />
    </linearGradient>
    <linearGradient id="meteorTailCyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0" />
      <stop offset="25%" stop-color="{CYAN}" stop-opacity="0.30" />
      <stop offset="65%" stop-color="#7DD3FC" stop-opacity="0.75" />
      <stop offset="90%" stop-color="#E0F2FE" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="1" />
    </linearGradient>
    <linearGradient id="meteorTailCore" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0" />
      <stop offset="60%" stop-color="#FFFFFF" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="1" />
    </linearGradient>
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>"""


def _meteor_css() -> str:
    return """      .meteor {
        opacity: 0;
        animation: shoot 3.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
      }
      .m1 { animation-duration: 3.2s; animation-delay: 0.2s; }
      .m2 { animation-duration: 4.0s; animation-delay: 1.4s; }
      .m3 { animation-duration: 3.6s; animation-delay: 2.4s; }
      .m4 { animation-duration: 4.4s; animation-delay: 0.8s; }
      @keyframes shoot {
        0% {
          transform: translateX(0) scaleX(0.35);
          opacity: 0;
        }
        10% {
          opacity: 1;
          transform: translateX(70px) scaleX(1);
        }
        65% {
          opacity: 0.95;
        }
        100% {
          transform: translateX(540px) scaleX(0.5);
          opacity: 0;
        }
      }"""


def _meteor(
    x: int,
    y: int,
    angle: float,
    tail_id: str,
    meteor_cls: str,
    length: int = 130,
    width: float = 2.4,
    color: str = GOLD,
) -> str:
    return f"""    <g transform="translate({x}, {y}) rotate({angle})">
      <g class="meteor {meteor_cls}">
        <polygon points="-{length * 1.05:.0f},0 0,-{width * 1.6:.1f} 0,{width * 1.6:.1f}" fill="url(#{tail_id})" opacity=".38" />
        <polygon points="-{length},0 0,-{width:.1f} 0,{width:.1f}" fill="url(#{tail_id})" />
        <polygon points="-{length * 0.55:.0f},0 0,-{width * 0.5:.1f} 0,{width * 0.5:.1f}" fill="url(#meteorTailCore)" opacity=".85" />
        <circle cx="0" cy="0" r="{width * 2.0:.1f}" fill="{color}" opacity=".35" />
        <circle cx="0" cy="0" r="{width * 1.25:.1f}" fill="{color}" opacity=".7" />
        <circle cx="0" cy="0" r="{width * 0.9:.1f}" fill="#FFFFFF" filter="url(#glow)" />
      </g>
    </g>"""


def _hero_sun(avatar: str) -> str:
    return f"""    <g>
      <circle r="88" fill="url(#sunGlow)" class="breathe"/>
      <circle r="60" fill="none" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1" class="solar-wave"/>
      <circle r="60" fill="none" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1" class="solar-wave solar-wave-2"/>
      <circle r="54" fill="url(#sunGlow)" opacity=".82"/>
      <circle r="47" fill="#050810"/>
      <g clip-path="url(#sunClip)">
        <image href="{avatar}" x="-44" y="-44" width="88" height="88" preserveAspectRatio="xMidYMid slice"/>
        <circle r="44" fill="url(#sunShade)"/>
      </g>
      <circle r="46" fill="none" stroke="{GOLD}" stroke-width="2"/>
      <circle r="51" fill="none" stroke="{GOLD}" stroke-opacity=".34" stroke-width="1" stroke-dasharray="3 7" class="sun-ring"/>
    </g>"""


def _orbiting_planet(index: int, p: content.Planet) -> str:
    body = max(7.0, p.radius / 15.0)
    halo = p.radius / 8.0 + 6.0
    moons = ""
    if p.moons:
        moon_orbit = body + 8.5
        moon_dots = []
        for m_idx in range(p.moons):
            moon_angle = math.radians(-58 + m_idx * (360 / max(1, p.moons)))
            mx = moon_orbit * math.cos(moon_angle)
            my = moon_orbit * math.sin(moon_angle)
            moon_dots.append(
                f'            <circle cx="{mx:.1f}" cy="{my:.1f}" r="1.7" fill="{INK}" opacity=".92"/>'
            )
        moons = (
            f'\n          <circle r="{moon_orbit:.1f}" fill="none" stroke="{p.color}" '
            f'stroke-opacity=".28" stroke-width=".75" stroke-dasharray="1.5 3"/>'
            f'\n          <g class="moon-orbit-{index}">\n'
            + "\n".join(moon_dots)
            + "\n          </g>"
        )
    return f"""    <g transform="rotate({p.angle})">
      <g class="planet-orbit-{index}">
        <g transform="translate({p.radius} 0)">
          <circle r="{halo:.1f}" fill="{p.color}" opacity=".14" class="planet-halo"/>
          <circle r="{body:.1f}" fill="{p.color}"/>
          <circle r="{body:.1f}" fill="url(#sphere)"/>
          <circle r="{body:.1f}" fill="none" stroke="{p.color}" stroke-opacity=".75"/>{moons}
        </g>
      </g>
    </g>"""


def build_hero() -> str:
    avatar = _avatar_data_uri()
    orbits = "\n".join(
        f'    <circle class="orbit orbit-track-{i}" r="{p.radius}" stroke="{TRACK}" '
        f'stroke-width="1" stroke-dasharray="2 7"/>'
        for i, p in enumerate(content.PLANETS)
    )
    planets = "\n".join(
        _orbiting_planet(i, p) for i, p in enumerate(content.PLANETS)
    )

    orbit_css = []
    for i in range(len(content.PLANETS)):
        period = PLANET_PERIODS[i % len(PLANET_PERIODS)]
        moon_period = MOON_PERIODS[i % len(MOON_PERIODS)]
        direction = "orbit-cw" if i % 2 == 0 else "orbit-ccw"
        moon_dir = "orbit-ccw" if i % 2 == 0 else "orbit-cw"
        dash_dir = "dash-flow" if i % 2 == 0 else "dash-flow-rev"
        orbit_css.append(
            f"      .planet-orbit-{i} {{ transform-origin: 0px 0px; animation: {direction} {period}s linear infinite; }}"
        )
        orbit_css.append(
            f"      .moon-orbit-{i} {{ transform-origin: 0px 0px; animation: {moon_dir} {moon_period:g}s linear infinite; }}"
        )
        orbit_css.append(
            f"      .orbit-track-{i} {{ animation: {dash_dir} {18 + i * 6}s linear infinite; }}"
        )
    orbit_css_block = "\n".join(orbit_css)
    reduced_selectors = ", ".join(
        [
            ".rise",
            ".fade",
            ".breathe",
            ".solar-wave",
            ".solar-wave-2",
            ".sun-ring",
            ".beacon-pulse",
            ".planet-halo",
            ".star-drift",
            ".meteor",
            ".twinkle-a",
            ".twinkle-b",
            ".twinkle-c",
            ".twinkle-d",
            *(f".planet-orbit-{i}" for i in range(len(content.PLANETS))),
            *(f".moon-orbit-{i}" for i in range(len(content.PLANETS))),
            *(f".orbit-track-{i}" for i in range(len(content.PLANETS))),
        ]
    )

    body = f"""  <defs>
    <radialGradient id="space" cx="50%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#0B1830"/>
      <stop offset="48%" stop-color="#060C18"/>
      <stop offset="100%" stop-color="{BG}"/>
    </radialGradient>
    <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{GOLD}" stop-opacity=".58"/>
      <stop offset="42%" stop-color="#FF7A3D" stop-opacity=".26"/>
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
{_meteor_defs()}
    <clipPath id="sunClip"><circle r="44"/></clipPath>
    <clipPath id="heroBounds"><rect width="880" height="520" rx="16"/></clipPath>
    <style>
      .rise {{ animation: rise 900ms cubic-bezier(.2,.7,.2,1) both; }}
      .d1 {{ animation-delay: 80ms; }}
      .d2 {{ animation-delay: 170ms; }}
      .d3 {{ animation-delay: 260ms; }}
      .fade {{ animation: fade 1100ms ease-out 350ms both; }}
      .breathe {{ animation: breathe 5.5s ease-in-out infinite; }}
      .solar-wave {{ transform-origin: 0px 0px; animation: solarWave 4.8s ease-out infinite; }}
      .solar-wave-2 {{ animation-delay: 2.4s; }}
      .sun-ring {{ transform-origin: 0px 0px; animation: orbit-cw 44s linear infinite; }}
      .beacon-pulse {{ animation: beacon 2.4s ease-in-out infinite; }}
      .planet-halo {{ animation: haloPulse 4.2s ease-in-out infinite; }}
      .star-drift {{ animation: starDrift 18s ease-in-out infinite; }}
{_meteor_css()}
      .twinkle-a {{ animation: twinkle 3.8s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 5.2s ease-in-out 1.1s infinite; }}
      .twinkle-c {{ animation: twinkle 6.4s ease-in-out 2.2s infinite; }}
      .twinkle-d {{ animation: twinkle 4.6s ease-in-out 0.6s infinite; }}
{orbit_css_block}
      @keyframes rise {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
      @keyframes breathe {{
        0%, 100% {{ opacity: .60; }}
        50% {{ opacity: .96; }}
      }}
      @keyframes solarWave {{
        0% {{ transform: scale(0.84); opacity: .45; }}
        100% {{ transform: scale(1.42); opacity: 0; }}
      }}
      @keyframes beacon {{
        0%, 100% {{ opacity: .55; }}
        50% {{ opacity: 1; }}
      }}
      @keyframes haloPulse {{
        0%, 100% {{ opacity: .10; }}
        50% {{ opacity: .24; }}
      }}
      @keyframes orbit-cw {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
      }}
      @keyframes orbit-ccw {{
        from {{ transform: rotate(360deg); }}
        to {{ transform: rotate(0deg); }}
      }}
      @keyframes dash-flow {{
        from {{ stroke-dashoffset: 0; }}
        to {{ stroke-dashoffset: -72; }}
      }}
      @keyframes dash-flow-rev {{
        from {{ stroke-dashoffset: 0; }}
        to {{ stroke-dashoffset: 72; }}
      }}
      @keyframes starDrift {{
        0%, 100% {{ transform: translate(0px, 0px); }}
        50% {{ transform: translate(4px, -3px); }}
      }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: .18; }}
        50% {{ opacity: .92; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        {reduced_selectors} {{
          animation: none !important;
        }}
        .rise, .fade {{ opacity: 1; transform: none; }}
        .meteor {{ display: none; }}
      }}
    </style>
  </defs>

  <g clip-path="url(#heroBounds)">
    <rect width="880" height="520" rx="16" fill="url(#space)"/>
    <g class="fade">
      <g class="star-drift">
{_dust_stars()}
      </g>
{_stars()}
    </g>

    <g class="rise d1">
      <circle cx="49" cy="41" r="4" fill="{GOLD}" class="beacon-pulse"/>
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
{_hero_sun(avatar)}
{planets}
    </g>

{_meteor(780, -30, 126, "meteorTailGold", "m1", length=130, width=2.4, color=GOLD)}
{_meteor(530, -35, 124, "meteorTailCyan", "m2", length=130, width=2.2, color=CYAN)}
{_meteor(860, 60, 128, "meteorTailGold", "m3", length=130, width=2.2, color=GOLD)}
  </g>
  <rect x=".5" y=".5" width="879" height="519" rx="15.5" stroke="{BORDER}"/>
"""
    return svg(880, 520, content.HERO_ALT, content.HERO_DESC, body)


def _pill(x: float, y: float, label: str, color: str, index: int) -> tuple[str, float]:
    width = max(78, len(label) * 6.2 + 24)
    body = (
        f'  <g class="pill-glow pill-{index}">\n'
        f'    <rect x="{x:g}" y="{y:g}" width="{width:.1f}" height="23" rx="4" '
        f'fill="{SURFACE}" stroke="{BORDER}"/>\n'
        f'    <circle cx="{x + 9:g}" cy="{y + 11.5:g}" r="2" fill="{color}" class="beacon"/>\n'
        + "    "
        + text(
            x + width / 2 + 3,
            y + 15,
            label,
            size=9.5,
            fill=color,
            family=MONO,
            weight=700,
            anchor="middle",
            spacing=.3,
        )
        + "\n  </g>"
    )
    return body, width


def build_about() -> str:
    avatar = _avatar_data_uri()
    pills = []
    x = 170.0
    for idx, (label, color) in enumerate(content.FACTS):
        markup, width = _pill(x, 170, label, color, idx)
        pills.append(markup)
        x += width + 10
    about_stars = _micro_stars(
        (
            (784, 34, 0.9, "a"),
            (832, 62, 1.1, "b"),
            (748, 86, 0.7, "c"),
            (848, 128, 0.8, "a"),
            (806, 178, 1.0, "b"),
            (28, 30, 0.7, "c"),
            (36, 184, 0.8, "a"),
        )
    )
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
{_meteor_defs()}
    <clipPath id="aboutClip"><circle r="46"/></clipPath>
    <clipPath id="aboutBounds"><rect width="880" height="214" rx="14"/></clipPath>
    <style>
      .breathe {{ animation: breathe 5.5s ease-in-out infinite; }}
      .ring-spin {{ transform-origin: 0px 0px; animation: spin 26s linear infinite; }}
      .sat-orbit {{ transform-origin: 0px 0px; animation: spin 11s linear infinite; }}
      .beacon {{ animation: beacon 2.6s ease-in-out infinite; }}
      .twinkle-a {{ animation: twinkle 3.8s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 5.2s ease-in-out 1.2s infinite; }}
      .twinkle-c {{ animation: twinkle 6.4s ease-in-out 2.1s infinite; }}
      .pill-0 {{ animation: pillPulse 6s ease-in-out 0s infinite; }}
      .pill-1 {{ animation: pillPulse 6s ease-in-out 1.5s infinite; }}
      .pill-2 {{ animation: pillPulse 6s ease-in-out 3.0s infinite; }}
      .pill-3 {{ animation: pillPulse 6s ease-in-out 4.5s infinite; }}
{_meteor_css()}
      @keyframes breathe {{ 0%, 100% {{ opacity: .62; }} 50% {{ opacity: .96; }} }}
      @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
      @keyframes beacon {{ 0%, 100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
      @keyframes twinkle {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .85; }} }}
      @keyframes pillPulse {{ 0%, 100% {{ opacity: .86; }} 50% {{ opacity: 1; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .breathe, .ring-spin, .sat-orbit, .beacon, .twinkle-a, .twinkle-b, .twinkle-c,
        .pill-0, .pill-1, .pill-2, .pill-3, .meteor {{ animation: none !important; }}
        .meteor {{ display: none; }}
      }}
    </style>
  </defs>

  <g clip-path="url(#aboutBounds)">
    <rect width="880" height="214" rx="14" fill="{PANEL}"/>
    <g>
{about_stars}
    </g>
{_meteor(760, -25, 126, "meteorTailGold", "m1", length=130, width=2.4, color=GOLD)}
{_meteor(490, -30, 124, "meteorTailCyan", "m2", length=130, width=2.2, color=CYAN)}

    <g transform="translate(88 105)">
      <circle r="64" fill="url(#aboutGlow)" class="breathe"/>
      <circle r="55" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="3 6" class="ring-spin"/>
      <g class="sat-orbit">
        <circle cx="55" cy="0" r="2.4" fill="{GOLD}"/>
        <circle cx="55" cy="0" r="5" fill="{GOLD}" opacity=".25"/>
      </g>
      <circle r="48" fill="#050810"/>
      <g clip-path="url(#aboutClip)">
        <image href="{avatar}" x="-46" y="-46" width="92" height="92" preserveAspectRatio="xMidYMid slice"/>
        <circle r="46" fill="url(#aboutShade)"/>
      </g>
      <circle r="48" fill="none" stroke="{GOLD}" stroke-width="2"/>
    </g>

    <g>
      <circle cx="172" cy="38" r="3" fill="{GOLD}" class="beacon"/>
      {text(182, 42, "THE SUN // ABOUT", size=10, fill=GOLD, family=MONO, weight=700, spacing=1.4)}
      {text(170, 84, content.NAME, size=28, weight=800, spacing=-.4)}
      {text(170, 108, "Software engineer / AI developer / CS '28 Andhra University", size=12, fill=MUTED, family=MONO)}
      {text(170, 134, content.ABOUT_QUOTE[0], size=12.5, fill=MUTED)}
      {text(170, 152, content.ABOUT_QUOTE[1], size=12.5, fill=MUTED)}
    </g>
    <g>
{chr(10).join(pills)}
    </g>
  </g>
  <rect x=".5" y=".5" width="879" height="213" rx="13.5" stroke="{BORDER}"/>
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
    # Deterministic per-project orbit period so the 4 cards move out of phase
    seed = sum(ord(ch) for ch in project.name)
    orbit_dur = 7.5 + (seed % 5) * 1.4
    ring_dur = 18 + (seed % 4) * 4
    body = f"""  <defs>
    <linearGradient id="accentBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{project.accent}" stop-opacity=".95"/>
      <stop offset="50%" stop-color="{INK}" stop-opacity=".85"/>
      <stop offset="100%" stop-color="{project.accent}" stop-opacity=".95"/>
    </linearGradient>
    <style>
      .moon-spin {{ transform-origin: 0px 0px; animation: spin {orbit_dur:.1f}s linear infinite; }}
      .ring-spin {{ transform-origin: 0px 0px; animation: spinRev {ring_dur}s linear infinite; }}
      .pulse {{ animation: pulse 3.2s ease-in-out infinite; }}
      .halo {{ animation: haloSoft 3.2s ease-in-out infinite; }}
      .arrow-nudge {{ animation: nudge 2.8s ease-in-out infinite; }}
      .twinkle-a {{ animation: twinkle 4.2s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 5.6s ease-in-out 1.4s infinite; }}
      @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
      @keyframes spinRev {{ from {{ transform: rotate(360deg); }} to {{ transform: rotate(0deg); }} }}
      @keyframes pulse {{ 0%, 100% {{ opacity: .55; }} 50% {{ opacity: 1; }} }}
      @keyframes haloSoft {{ 0%, 100% {{ opacity: .12; }} 50% {{ opacity: .32; }} }}
      @keyframes nudge {{ 0%, 100% {{ transform: translate(0px, 0px); opacity: .65; }} 50% {{ transform: translate(2px, -2px); opacity: 1; }} }}
      @keyframes twinkle {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .75; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .moon-spin, .ring-spin, .pulse, .halo, .arrow-nudge, .twinkle-a, .twinkle-b {{ animation: none !important; }}
      }}
    </style>
  </defs>

  <rect width="430" height="168" rx="11" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="429" height="167" rx="10.5" stroke="{BORDER}"/>
  <rect width="3.5" height="168" rx="1.75" fill="{project.accent}" class="pulse"/>

  <circle cx="332" cy="144" r="0.9" fill="{INK}" opacity=".35" class="twinkle-a"/>
  <circle cx="398" cy="128" r="1.0" fill="{project.accent}" opacity=".45" class="twinkle-b"/>
  <circle cx="408" cy="84" r="0.7" fill="{INK}" opacity=".3" class="twinkle-a"/>

  <g transform="translate(366 42)">
    <circle r="15" fill="none" stroke="{project.accent}" stroke-opacity=".26" stroke-width=".9" stroke-dasharray="2.5 4" class="ring-spin"/>
    <circle r="5" fill="{project.accent}" opacity=".18" class="halo"/>
    <circle r="3.2" fill="{project.accent}"/>
    <g class="moon-spin">
      <circle cx="15" cy="0" r="2" fill="{INK}"/>
      <circle cx="15" cy="0" r="4" fill="{project.accent}" opacity=".28"/>
    </g>
  </g>

  <g transform="translate(20 27)">
    {text(0, 0, project.moon, size=8.5, fill=project.accent, family=MONO, weight=700, spacing=.6)}
    <g transform="translate(388 0)">
      <g class="arrow-nudge">
        {text(0, 0, "↗", size=14, fill=FAINT, anchor="end")}
      </g>
    </g>
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
    row_css = []
    for index, planet in enumerate(content.PLANETS):
        y = 62 + index * 31
        cy = y - 4
        spin_dur = 6 + index * 2.5
        sig_dur = 2.6 + index * 0.45
        sig_delay = index * 0.35
        row_css.append(
            f"      .mini-orbit-{index} {{ transform-origin: 0px 0px; animation: spin {spin_dur:.1f}s linear infinite; }}"
        )
        row_css.append(
            f"      .sig-dot-{index} {{ animation: slidePulse {sig_dur:.2f}s ease-in-out {sig_delay:.2f}s infinite; }}"
        )
        row_css.append(
            f"      .conduit-{index} {{ animation: dashCrawl {3.5 + index * 0.6:.1f}s linear infinite; }}"
        )
        rows.append(
            f"""  <g>
    <g transform="translate(34 {cy})">
      <circle r="8.5" fill="none" stroke="{planet.color}" stroke-opacity=".28" stroke-width=".8" stroke-dasharray="2 3"/>
      <g class="mini-orbit-{index}">
        <circle cx="8.5" cy="0" r="1.4" fill="{INK}" opacity=".9"/>
      </g>
      <circle r="4.5" fill="{planet.color}"/>
      <circle r="6.5" fill="{planet.color}" opacity=".16" class="halo"/>
    </g>
    {text(50, y, planet.name, size=12.5, weight=700)}
    {text(168, y, planet.orbit, size=9.5, fill=planet.color, family=MONO)}
    <line x1="268" y1="{cy}" x2="298" y2="{cy}" stroke="{planet.color}" stroke-opacity=".45" stroke-width="1.5" stroke-dasharray="4 4" class="conduit-{index}"/>
    <circle cx="268" cy="{cy}" r="2.2" fill="{planet.color}" class="sig-dot-{index}"/>
    <circle cx="298" cy="{cy}" r="2" fill="{planet.color}"/>
    {text(308, y, planet.domain, size=10, fill=MUTED)}
    {text(654, y, planet.evidence, size=9.5, fill=planet.color, family=MONO)}
  </g>"""
        )

    stack_stars = _micro_stars(
        (
            (812, 26, 0.8, "a"),
            (844, 72, 1.0, "b"),
            (826, 134, 0.7, "c"),
            (850, 198, 0.9, "a"),
            (618, 212, 0.8, "b"),
        )
    )
    reduced_rows = ", ".join(
        [
            ".pulse",
            ".halo",
            ".twinkle-a",
            ".twinkle-b",
            ".twinkle-c",
            *(f".mini-orbit-{i}" for i in range(len(content.PLANETS))),
            *(f".sig-dot-{i}" for i in range(len(content.PLANETS))),
            *(f".conduit-{i}" for i in range(len(content.PLANETS))),
        ]
    )
    body = f"""  <defs>
{_meteor_defs()}
    <clipPath id="stackBounds"><rect width="880" height="226" rx="14"/></clipPath>
    <style>
      .pulse {{ animation: pulse 3s ease-in-out infinite; }}
      .halo {{ animation: haloSoft 3.4s ease-in-out infinite; }}
      .twinkle-a {{ animation: twinkle 3.8s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 5.0s ease-in-out 1.1s infinite; }}
      .twinkle-c {{ animation: twinkle 6.2s ease-in-out 2.0s infinite; }}
{_meteor_css()}
{chr(10).join(row_css)}
      @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
      @keyframes pulse {{ 0%, 100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
      @keyframes haloSoft {{ 0%, 100% {{ opacity: .10; }} 50% {{ opacity: .30; }} }}
      @keyframes twinkle {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .82; }} }}
      @keyframes dashCrawl {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -16; }} }}
      @keyframes slidePulse {{
        0% {{ transform: translateX(0px); opacity: 0; }}
        15% {{ opacity: 1; }}
        85% {{ opacity: 1; }}
        100% {{ transform: translateX(30px); opacity: 0; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        {reduced_rows}, .meteor {{ animation: none !important; }}
        .meteor {{ display: none; }}
      }}
    </style>
  </defs>

  <g clip-path="url(#stackBounds)">
    <rect width="880" height="226" rx="14" fill="{PANEL}"/>
    <g>
{stack_stars}
    </g>
{_meteor(780, -25, 126, "meteorTailCyan", "m1", length=130, width=2.4, color=CYAN)}
{_meteor(470, -30, 124, "meteorTailGold", "m2", length=130, width=2.2, color=GOLD)}

    <g transform="translate(28 29)">
      <circle cx="5" cy="5" r="4" fill="{GOLD}" class="pulse"/>
      {text(18, 9, "THE PLANETS // LANGUAGES & ORBITS", size=10, fill=GOLD, family=MONO, weight=700, spacing=1.2)}
    </g>
    <line x1="28" y1="44" x2="852" y2="44" stroke="{BORDER}"/>

{chr(10).join(rows)}

    {text(28, 214, "Orbit order is a reading order, not a ranking.", size=9, fill=FAINT, family=MONO)}
  </g>
  <rect x=".5" y=".5" width="879" height="225" rx="13.5" stroke="{BORDER}"/>
"""
    return svg(
        880,
        226,
        "Languages and orbits",
        "Five languages, the kind of work each one supports, and the projects that use them.",
        body,
    )


def _stat_box(
    x: int,
    label: str,
    big: str,
    small: str,
    color: str,
    index: int,
    big_size: float = 21.5,
) -> str:
    return f"""  <g transform="translate({x} 48)">
    <rect width="195" height="80" rx="7" fill="{SURFACE}" stroke="{BORDER}"/>
    <rect x="0" y="77" width="195" height="3" rx="1.5" fill="{color}" opacity=".45" class="bar-{index}"/>
    <circle cx="179" cy="18" r="2.6" fill="{color}" class="dot-{index}"/>
    <circle cx="179" cy="18" r="6" fill="none" stroke="{color}" stroke-opacity=".35" stroke-width=".8" class="ping-{index}"/>
    {text(16, 23, label, size=9, fill=MUTED, family=MONO, spacing=.7)}
    {text(16, 56, big, size=big_size, fill=color, weight=800, spacing=-.4)}
    {text(16, 72, small, size=9.5, fill=MUTED, family=MONO)}
  </g>"""


def build_log() -> str:
    log_stars = _micro_stars(
        (
            (760, 22, 0.8, "a"),
            (814, 28, 1.0, "b"),
            (848, 20, 0.7, "a"),
        )
    )
    body = f"""  <defs>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{GOLD}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{GOLD}" stop-opacity=".85"/>
      <stop offset="100%" stop-color="{GOLD}" stop-opacity="0"/>
    </linearGradient>
{_meteor_defs()}
    <clipPath id="logClip"><rect width="880" height="148" rx="14"/></clipPath>
    <style>
      .beacon {{ animation: pulse 2.4s ease-in-out infinite; }}
      .scan {{ animation: scan 7s linear infinite; }}
      .twinkle-a {{ animation: twinkle 3.8s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 5.2s ease-in-out 1.4s infinite; }}
      .dot-0 {{ animation: pulse 2.6s ease-in-out 0s infinite; }}
      .dot-1 {{ animation: pulse 2.6s ease-in-out .65s infinite; }}
      .dot-2 {{ animation: pulse 2.6s ease-in-out 1.3s infinite; }}
      .dot-3 {{ animation: pulse 2.6s ease-in-out 1.95s infinite; }}
      .ping-0 {{ transform-origin: 179px 18px; animation: ping 3.2s ease-out 0s infinite; }}
      .ping-1 {{ transform-origin: 179px 18px; animation: ping 3.2s ease-out .8s infinite; }}
      .ping-2 {{ transform-origin: 179px 18px; animation: ping 3.2s ease-out 1.6s infinite; }}
      .ping-3 {{ transform-origin: 179px 18px; animation: ping 3.2s ease-out 2.4s infinite; }}
      .bar-0 {{ animation: barGlow 4.4s ease-in-out 0s infinite; }}
      .bar-1 {{ animation: barGlow 4.4s ease-in-out 1.1s infinite; }}
      .bar-2 {{ animation: barGlow 4.4s ease-in-out 2.2s infinite; }}
      .bar-3 {{ animation: barGlow 4.4s ease-in-out 3.3s infinite; }}
{_meteor_css()}
      @keyframes pulse {{ 0%, 100% {{ opacity: .45; }} 50% {{ opacity: 1; }} }}
      @keyframes twinkle {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .8; }} }}
      @keyframes scan {{
        0% {{ transform: translateX(-140px); opacity: 0; }}
        10% {{ opacity: .9; }}
        90% {{ opacity: .9; }}
        100% {{ transform: translateX(880px); opacity: 0; }}
      }}
      @keyframes ping {{
        0% {{ transform: scale(0.5); opacity: .7; }}
        100% {{ transform: scale(1.9); opacity: 0; }}
      }}
      @keyframes barGlow {{ 0%, 100% {{ opacity: .25; }} 50% {{ opacity: .82; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .beacon, .scan, .twinkle-a, .twinkle-b,
        .dot-0, .dot-1, .dot-2, .dot-3,
        .ping-0, .ping-1, .ping-2, .ping-3,
        .bar-0, .bar-1, .bar-2, .bar-3, .meteor {{ animation: none !important; }}
        .scan {{ display: none; }}
        .meteor {{ display: none; }}
      }}
    </style>
  </defs>

  <g clip-path="url(#logClip)">
    <rect width="880" height="148" rx="14" fill="{PANEL}"/>
    <g>
{log_stars}
    </g>
{_meteor(790, -20, 126, "meteorTailGold", "m1", length=130, width=2.4, color=GOLD)}
{_meteor(510, -25, 124, "meteorTailCyan", "m2", length=130, width=2.2, color=CYAN)}

    <g transform="translate(28 29)">
      <circle cx="5" cy="5" r="4" fill="{GOLD}" class="beacon"/>
      {text(18, 9, "SOLAR LOG // CURRENT ORBIT", size=10, fill=GOLD, family=MONO, weight=700, spacing=1.2)}
    </g>
    <line x1="28" y1="42" x2="852" y2="42" stroke="{BORDER}"/>
    <rect x="0" y="41" width="140" height="2" fill="url(#scanGrad)" class="scan"/>

{_stat_box(28, "CURRENT ORBIT", "AI INTERN", "Aegion Dynamic", "#4CC9F0", 0)}
{_stat_box(238, "COMMUNITY", "185K+", "Mecha Break", "#C084FC", 1)}
{_stat_box(448, "PODIUM", "1ST PLACE", "HackMe 2024", "#F472B6", 2)}
{_stat_box(658, "BASED IN", "Visakhapatnam", "India / UTC+05:30", "#FB923C", 3)}
  </g>
  <rect x=".5" y=".5" width="879" height="147" rx="13.5" stroke="{BORDER}"/>
"""
    return svg(
        880,
        148,
        "Current orbit and record",
        "AI developer intern at Aegion Dynamic Solutions, 185,000-person community moderator, first place at HackMe 2024, based in Visakhapatnam.",
        body,
    )


def build_footer() -> str:
    body = f"""  <defs>
    <style>
      .beacon-core {{ animation: corePulse 2.4s ease-in-out infinite; }}
      .ripple-1 {{ transform-origin: 44px 43px; animation: ripple 3.2s ease-out infinite; }}
      .ripple-2 {{ transform-origin: 44px 43px; animation: ripple 3.2s ease-out 1.6s infinite; }}
      .wave-line {{ animation: waveFlow 3s linear infinite; }}
      .cta-pulse {{ animation: ctaGlow 3.2s ease-in-out infinite; }}
      .twinkle-a {{ animation: twinkle 4.2s ease-in-out infinite; }}
      .twinkle-b {{ animation: twinkle 5.4s ease-in-out 1.5s infinite; }}
      @keyframes corePulse {{ 0%, 100% {{ opacity: .65; }} 50% {{ opacity: 1; }} }}
      @keyframes ripple {{
        0% {{ transform: scale(0.55); opacity: .75; }}
        100% {{ transform: scale(1.75); opacity: 0; }}
      }}
      @keyframes waveFlow {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -24; }} }}
      @keyframes ctaGlow {{ 0%, 100% {{ stroke-opacity: .65; }} 50% {{ stroke-opacity: 1; }} }}
      @keyframes twinkle {{ 0%, 100% {{ opacity: .15; }} 50% {{ opacity: .75; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .beacon-core, .ripple-1, .ripple-2, .wave-line, .cta-pulse, .twinkle-a, .twinkle-b {{
          animation: none !important;
        }}
      }}
    </style>
  </defs>

  <rect width="880" height="86" rx="12" fill="{PANEL}"/>
  <rect x=".5" y=".5" width="879" height="85" rx="11.5" stroke="{BORDER}"/>

  <circle cx="596" cy="22" r="0.9" fill="{INK}" opacity=".35" class="twinkle-a"/>
  <circle cx="642" cy="64" r="1.0" fill="{GOLD}" opacity=".4" class="twinkle-b"/>
  <circle cx="684" cy="26" r="0.8" fill="{INK}" opacity=".3" class="twinkle-a"/>

  <circle cx="44" cy="43" r="17" fill="{SURFACE}" stroke="{GOLD}" stroke-opacity=".6"/>
  <circle cx="44" cy="43" r="17" fill="none" stroke="{GOLD}" stroke-width="1.2" class="ripple-1"/>
  <circle cx="44" cy="43" r="17" fill="none" stroke="{GOLD}" stroke-width="1.2" class="ripple-2"/>
  <circle cx="44" cy="43" r="6" fill="{GOLD}" class="beacon-core"/>

  {text(76, 38, "Let's build something that has to keep up.", size=15.5, weight=800)}
  {text(76, 58, f"{content.EMAIL} / {content.LOCATION} / UTC+05:30", size=10, fill=MUTED, family=MONO)}

  <line x1="556" y1="43" x2="704" y2="43" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="4 8" class="wave-line"/>

  <g transform="translate(715 28)">
    <rect width="137" height="30" rx="4" fill="{SURFACE}" stroke="{GOLD}" stroke-width="1.2" class="cta-pulse"/>
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