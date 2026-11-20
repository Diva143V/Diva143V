"""Builds the single hero SVG.

The hero is a nameplate, not an infographic. It carries only two things that
must survive a 350px-wide phone screen: the name and one caption line. The
caption-track marks on the right are deliberately wordless so nothing in this
file can clip or become unreadable when GitHub scales it down.
"""

from __future__ import annotations

import base64
import html
from pathlib import Path
from string import Template

from content import NAME_LINES, TAGLINE_LINES, HERO_ALT, HERO_DESC

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"

BG = "#0F1216"
INK = "#E6EAF0"
DIM = "#8B96A5"
RULE = "#232B34"
YELLOW = "#FFD24C"
CYAN = "#4FD6E8"

# Cue widths for the three caption-track rows. They are read left to right,
# like subtitle segments on a timeline; no text is used, so no font can clip.
TRACK_ROWS = (
    (44, 76, 28, 60, 16),
    (30, 96, 52, 54),
    (58, 36, 74, 26, 30),
)
TRACK_X = 576
TRACK_WIDTH = 256
TRACK_ROW_GAP = 74
TRACK_FIRST_BASELINE = 168

TEMPLATE = Template(
    """<svg width="880" height="480" viewBox="0 0 880 480" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="hero-title hero-desc">
  <title id="hero-title">$alt</title>
  <desc id="hero-desc">$desc</desc>
  <defs>
    <style>
      @font-face {
        font-family: 'Archivo';
        font-style: normal;
        font-weight: 800;
        font-display: swap;
        src: url(data:font/woff2;base64,$archivo) format('woff2');
      }
      @font-face {
        font-family: 'DM Mono';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(data:font/woff2;base64,$mono) format('woff2');
      }
      .display {
        font-family: 'Archivo', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 800;
      }
      .mono {
        font-family: 'DM Mono', ui-monospace, 'Cascadia Mono', Consolas, monospace;
        font-weight: 400;
      }
      .rise { animation: rise 900ms cubic-bezier(.2,.7,.2,1) both; }
      .d1 { animation-delay: 100ms; }
      .d2 { animation-delay: 200ms; }
      .d3 { animation-delay: 300ms; }
      .rule {
        animation: rule-in 700ms ease-out 40ms both;
        transform-box: view-box;
        transform-origin: 48px 66px;
      }
      .track { animation: fade-in 700ms ease-out 700ms both; }
      .caption { animation: rise 800ms cubic-bezier(.2,.7,.2,1) 850ms both; }
      .playhead { animation: sweep 16s linear 1500ms infinite both; }
      @keyframes rise {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes rule-in {
        from { opacity: 0; transform: scaleX(0); }
        to { opacity: 1; transform: scaleX(1); }
      }
      @keyframes fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      @keyframes sweep {
        0% { transform: translateX(0); opacity: 0; }
        6% { opacity: .65; }
        94% { opacity: .65; }
        100% { transform: translateX(256px); opacity: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .rise, .rule, .track, .caption {
          animation: none;
          opacity: 1;
          transform: none;
        }
        .playhead { display: none; }
      }
    </style>
  </defs>

  <rect width="880" height="480" rx="16" fill="$bg"/>
  <rect x="0.5" y="0.5" width="879" height="479" rx="15.5" stroke="$rule"/>

  <g class="rise d1">
    <circle cx="53" cy="40" r="5" fill="$yellow"/>
    <text x="68" y="45" class="display" font-size="15" letter-spacing="3.2" fill="$ink">DIVA</text>
  </g>

  <line class="rule" x1="48" y1="66.5" x2="832" y2="66.5" stroke="$rule"/>

  <g class="rise d1"><text id="name-1" x="46" y="178" class="display" font-size="96" letter-spacing="-2.5" fill="$ink">$name1</text></g>
  <g class="rise d2"><text id="name-2" x="46" y="266" class="display" font-size="96" letter-spacing="-2.5" fill="$ink">$name2</text></g>
  <g class="rise d3"><text id="name-3" x="46" y="354" class="display" font-size="96" letter-spacing="-2.5" fill="$yellow">$name3</text></g>

  <g class="track">
    $track
  </g>

  <g class="playhead">
    <line x1="576" y1="126" x2="576" y2="342" stroke="$yellow" stroke-width="1"/>
    <rect x="572" y="126" width="8" height="8" rx="1" fill="$yellow"/>
  </g>

  <g class="caption">
    <rect x="48" y="382" width="784" height="74" rx="6" fill="#080B0E" stroke="$rule"/>
    <rect x="48" y="382" width="3" height="74" rx="1.5" fill="$yellow"/>
    <text id="caption-1" x="70" y="412" class="mono" font-size="26" fill="$ink">$cap1</text>
    <text id="caption-2" x="70" y="440" class="mono" font-size="26" fill="$dim">$cap2</text>
    <rect x="782" y="410" width="34" height="18" rx="3" stroke="$yellow" opacity=".55"/>
    <text x="799" y="423" class="mono" font-size="11" text-anchor="middle" fill="$yellow">CC</text>
  </g>
</svg>
"""
)


def _font_data_uri(path: Path) -> str:
    with path.open("rb") as handle:
        return base64.b64encode(handle.read()).decode("ascii")


def _track_markup() -> str:
    marks: list[str] = []
    for row, widths in enumerate(TRACK_ROWS):
        baseline = TRACK_FIRST_BASELINE + row * TRACK_ROW_GAP
        marks.append(
            f'<line x1="{TRACK_X}" y1="{baseline}" x2="{TRACK_X + TRACK_WIDTH}" '
            f'y2="{baseline}" stroke="{RULE}"/>'
        )
        x = TRACK_X
        for column, width in enumerate(widths):
            if x + width > TRACK_X + TRACK_WIDTH:
                break
            opacity = "0.20" if (row + column) % 3 == 0 else "0.34"
            marks.append(
                f'<rect x="{x}" y="{baseline - 20}" width="{width}" height="11" '
                f'rx="3" fill="{CYAN}" opacity="{opacity}"/>'
            )
            x += width + 8
    return "\n    ".join(marks)


def build_hero_svg() -> str:
    return TEMPLATE.substitute(
        alt=html.escape(HERO_ALT, quote=False),
        desc=html.escape(HERO_DESC, quote=False),
        archivo=_font_data_uri(FONT_DIR / "archivo-800.woff2"),
        mono=_font_data_uri(FONT_DIR / "dmmono-400.woff2"),
        name1=html.escape(NAME_LINES[0], quote=False),
        name2=html.escape(NAME_LINES[1], quote=False),
        name3=html.escape(NAME_LINES[2], quote=False),
        cap1=html.escape(TAGLINE_LINES[0], quote=False),
        cap2=html.escape(TAGLINE_LINES[1], quote=False),
        track=_track_markup(),
        bg=BG,
        ink=INK,
        dim=DIM,
        rule=RULE,
        yellow=YELLOW,
    )
