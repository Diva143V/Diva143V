"""All editable copy and links for the solar-system profile.

`scripts/generate_solar.py` turns this file into README.md and the SVGs under
`assets/`. Nothing is fetched at build time, so every claim can be reviewed in
one place and the generated files stay deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass


NAME = "Diwakar Venkat Peddada"
USERNAME = "Diva143V"
EMAIL = "diwa.p2007@gmail.com"
LOCATION = "Visakhapatnam, India"

HERO_ALT = (
    "A solar-system portrait: Diwakar Venkat Peddada at the centre, five "
    "language planets in orbit, and the projects marked as moons."
)
HERO_DESC = (
    "A dark orbital chart. The name Diwakar Venkat Peddada sits on the left; "
    "on the right, an avatar of Diwakar is the sun, with Python, C#, Rust, "
    "TypeScript and C++ drawn as planets on five orbits. Small moon dots "
    "stand in for the projects built on top of them."
)
HERO_TAGLINE = (
    "I build the layer between a live signal",
    "and the person waiting for it.",
)
ABOUT_QUOTE = (
    "I build software that has to keep up: captions while someone is speaking,",
    "evidence while papers disagree, memory while an agent works.",
)
FACTS = (
    ("AI intern @ Aegion", "#4CC9F0"),
    ("185K community", "#C084FC"),
    ("1st place, HackMe 2024", "#F472B6"),
    (LOCATION, "#FB923C"),
)

INTRO = """I'm Diwakar, Diva to most people. I'm studying computer science at Andhra University and working as an AI developer intern at Aegion Dynamic Solutions. I live in Visakhapatnam, on the east coast of India.

Most of what I build starts with something that is already happening: a speaker who won't wait for the translation, a pile of papers that disagree, an agent that needs to remember a decision from six sessions ago. I like the part where a messy live feed turns into something a person can read at a glance.

I started on the front end, rebuilding React screens and learning to measure a render before calling it faster. I still care about that, but these days more of my time goes into Python pipelines, Windows overlays in C#, and Rust servers."""

SOLAR_NOTE = (
    "The map is a little theatrical: languages are planets, projects are moons, "
    "and I'm the sun in the middle. I kept it because it makes the stack easier "
    "to read at a glance."
)


@dataclass(frozen=True)
class Project:
    name: str
    url: str
    moon: str
    role: str
    subtitle: str
    body: tuple[str, str]
    tags: tuple[str, ...]
    accent: str
    alt: str


@dataclass(frozen=True)
class Planet:
    name: str
    orbit: str
    domain: str
    evidence: str
    color: str
    angle: int
    radius: int
    moons: int = 0


@dataclass(frozen=True)
class Role:
    title: str
    org: str
    period: str
    detail: str


PROJECTS = (
    Project(
        name="LiveSubs",
        url="https://github.com/Diva143V/LiveSubs",
        moon="MOON 01 // CAPTION OVERLAY",
        role="Windows captions",
        subtitle="Reads Windows Live Captions and translates them in place.",
        body=(
            "Sends the text through Google, DeepL, OpenAI or Ollama and pins both",
            "lines above any app. C# and WPF on .NET 8, shipped as one executable.",
        ),
        tags=("C#", "WPF", ".NET 8", "Windows"),
        accent="#4CC9F0",
        alt=(
            "LiveSubs card: a Windows caption overlay that translates Windows "
            "Live Captions through Google, DeepL, OpenAI or Ollama."
        ),
    ),
    Project(
        name="Griffin",
        url="https://github.com/Diva143V/Griffin",
        moon="MOON 02 // BIOMEDICAL EVIDENCE",
        role="Evidence workbench",
        subtitle="Collects biomedical papers and makes their claims comparable.",
        body=(
            "Ten sources in, ChromaDB retrieval and local-model extraction out,",
            "with contradictions surfaced instead of averaged away. Python and Reflex.",
        ),
        tags=("Python", "ChromaDB", "Ollama", "Reflex"),
        accent="#38BDF8",
        alt=(
            "Griffin card: a biomedical evidence workbench using ChromaDB, "
            "Ollama and Reflex."
        ),
    ),
    Project(
        name="Knox",
        url="https://github.com/Diva143V/Knox",
        moon="MOON 03 // AGENT MEMORY",
        role="MCP server",
        subtitle="Keeps decisions and context across coding sessions.",
        body=(
            "Eight tools over JSON-RPC, backed by a Rust graph core. The desktop",
            "app is Tauri and React, with SQLite underneath.",
        ),
        tags=("Rust", "MCP", "Tauri", "SQLite"),
        accent="#FF8A4C",
        alt=(
            "Knox card: a Rust MCP server and Tauri desktop app that keeps "
            "context across coding sessions."
        ),
    ),
    Project(
        name="SyGriffin",
        url="https://github.com/Diva143V/SyGriffin",
        moon="MOON 04 // NEOANTIGENS",
        role="Neoantigen CLI",
        subtitle="The vaccine-target pipeline built on Griffin.",
        body=(
            "Takes tumour VCF files and predicts vaccine-relevant targets with",
            "binding scores you can inspect. A fork of Griffin.",
        ),
        tags=("Python", "R", "VCF", "Neoantigen"),
        accent="#F472B6",
        alt=(
            "SyGriffin card: a neoantigen CLI that reads tumour VCF files and "
            "predicts vaccine-relevant targets. A fork of Griffin."
        ),
    ),
)

SMALLER = (
    "Smaller things: [Polaris](https://github.com/Diva143V/Kg-Library-API) "
    "(a Think-on-Graph knowledge graph library) and "
    "[myselfdiva](https://github.com/Diva143V/myselfdiva) (my portfolio)."
)

PLANETS = (
    Planet(
        name="Python",
        orbit="Orbit 1 / inner",
        domain="Biomedical RAG, local models, data pipelines",
        evidence="Griffin / SyGriffin",
        color="#38BDF8",
        angle=208,
        radius=60,
        moons=2,
    ),
    Planet(
        name="C# / .NET",
        orbit="Orbit 2",
        domain="Windows overlays, live captions, WPF",
        evidence="LiveSubs",
        color="#C084FC",
        angle=334,
        radius=94,
        moons=1,
    ),
    Planet(
        name="Rust",
        orbit="Orbit 3",
        domain="MCP server, graph core, Tauri",
        evidence="Knox",
        color="#FB923C",
        angle=154,
        radius=128,
        moons=1,
    ),
    Planet(
        name="TypeScript",
        orbit="Orbit 4",
        domain="React, Vite, interface work",
        evidence="myselfdiva",
        color="#60A5FA",
        angle=22,
        radius=162,
        moons=1,
    ),
    Planet(
        name="C++",
        orbit="Orbit 5 / outer",
        domain="Algorithms and data structures",
        evidence="HackMe 2024",
        color="#F472B6",
        angle=112,
        radius=196,
    ),
)

ROLES = (
    Role(
        title="AI developer intern",
        org="Aegion Dynamic Solutions",
        period="Jul 2026 to now",
        detail=(
            "Production LLM integrations, automation, and the unglamorous "
            "plumbing that makes them reliable."
        ),
    ),
    Role(
        title="Front-end developer intern",
        org="Aegion Dynamic Solutions",
        period="Aug to Oct 2025",
        detail=(
            "Rebuilt React interfaces, cut unnecessary renders, and tightened "
            "the handoff between the UI and the API."
        ),
    ),
    Role(
        title="Community moderator",
        org="Mecha Break",
        period="Mar 2024 to Jul 2025",
        detail=(
            "185,000 members. My job was turning a firehose of player reports "
            "into something the developers could act on."
        ),
    ),
)

CREDENTIALS = (
    "I took first place at HackMe 2024, solving their problem statement in C++, "
    "and completed the JPMorgan Chase software engineering simulation in 2026."
)

LINKS = (
    ("Portfolio", "https://myselfdiva.netlify.app/"),
    ("LinkedIn", "https://linkedin.com/in/diwakar-venkat-peddada-66aa30229/"),
    ("X", "https://x.com/Diva_2007_"),
    ("Email", f"mailto:{EMAIL}"),
)

CLOSING = (
    "If you're working on something where latency actually matters, my inbox is open."
)

README_HEADINGS = (
    "The moons",
    "The planets",
    "The solar log",
    "Transmission",
)


def all_repo_urls() -> set[str]:
    """Every GitHub repository URL the README is allowed to point at."""
    urls = {project.url for project in PROJECTS}
    urls.add("https://github.com/Diva143V/SyGriffin")
    urls.add("https://github.com/Diva143V/Kg-Library-API")
    urls.add("https://github.com/Diva143V/myselfdiva")
    urls.add(f"https://github.com/{USERNAME}/{USERNAME}")
    return urls
