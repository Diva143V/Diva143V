"""All editable copy and links for the profile live here.

`scripts/build_profile.py` turns this into README.md and assets/hero.svg.
Nothing in this file is fetched at build time, so the output is deterministic
and every claim can be checked in one place.
"""

from __future__ import annotations

from dataclasses import dataclass


NAME = "Diwakar Venkat Peddada"
USERNAME = "Diva143V"
EMAIL = "diwa.p2007@gmail.com"

# The hero sets the name as three stacked lines; the last one is accented.
NAME_LINES = ("DIWAKAR", "VENKAT", "PEDDADA")

# Two lines, because the hero is also viewed at 350px wide on a phone.
TAGLINE_LINES = (
    "I build the layer between a live signal",
    "and the person waiting for it.",
)
HERO_ALT = f"{NAME}. {' '.join(TAGLINE_LINES)}"
HERO_DESC = (
    "A dark broadcast-style nameplate: the name Diwakar Venkat Peddada above a "
    "caption line that reads, I build the layer between a live signal and the "
    "person waiting for it."
)


@dataclass(frozen=True)
class Project:
    name: str
    url: str
    body: str


@dataclass(frozen=True)
class Role:
    title: str
    org: str
    period: str
    detail: str


INTRO = """I'm Diwakar, Diva to most people. I'm studying computer science at Andhra University and working as an AI developer intern at Aegion Dynamic Solutions. I live in Visakhapatnam, on the east coast of India.

Most of what I build starts with something that is already happening: a speaker who won't wait for the translation, a pile of papers that disagree, an agent that needs to remember a decision from six sessions ago. I like the part where a messy live feed turns into something a person can read at a glance.

I started on the front end, rebuilding React screens and learning to measure a render before calling it faster. I still care about that, but these days more of my time goes into Python pipelines, Windows overlays in C#, and Rust servers."""


PROJECTS = (
    Project(
        name="LiveSubs",
        url="https://github.com/Diva143V/LiveSubs",
        body=(
            "is a caption overlay for Windows. It reads Windows Live Captions, sends the "
            "text through one of several translation backends (Google, DeepL, OpenAI, "
            "Ollama, and others), and keeps the original and translated lines pinned above "
            "whatever app is playing. It ships as a single executable, written in C# with "
            "WPF on .NET 8."
        ),
    ),
    Project(
        name="Griffin",
        url="https://github.com/Diva143V/Griffin",
        body=(
            "is a workbench for biomedical evidence. It collects from ten sources, embeds "
            "and retrieves papers with ChromaDB, extracts claims with local models, ranks "
            "the evidence, and flags papers that contradict each other. The neoantigen CLI "
            "is in [SyGriffin](https://github.com/Diva143V/SyGriffin), a fork of Griffin. "
            "Built with Python, Ollama, and Reflex."
        ),
    ),
    Project(
        name="Knox",
        url="https://github.com/Diva143V/Knox",
        body=(
            "is a knowledge graph for coding agents, with an MCP server on top. It keeps "
            "decisions and context across sessions and exposes eight tools over JSON-RPC. "
            "The desktop app is Tauri and React with SQLite underneath; the core is Rust."
        ),
    ),
)

SMALLER = (
    "Smaller things: [Polaris](https://github.com/Diva143V/Kg-Library-API) "
    "(a Think-on-Graph knowledge graph library) and "
    "[myselfdiva](https://github.com/Diva143V/myselfdiva) (my portfolio)."
)

EXTRA_REPOS = {
    "SyGriffin": "https://github.com/Diva143V/SyGriffin",
    "Kg-Library-API": "https://github.com/Diva143V/Kg-Library-API",
    "myselfdiva": "https://github.com/Diva143V/myselfdiva",
}


ROLES = (
    Role(
        title="AI developer intern",
        org="Aegion Dynamic Solutions",
        period="Jul 2026 to now",
        detail=(
            "Production LLM integrations, automation, and the unglamorous plumbing that "
            "makes them reliable."
        ),
    ),
    Role(
        title="Front-end developer intern",
        org="Aegion Dynamic Solutions",
        period="Aug to Oct 2025",
        detail=(
            "Rebuilt React interfaces, cut unnecessary renders, and tightened the handoff "
            "between the UI and the API."
        ),
    ),
    Role(
        title="Community moderator",
        org="Mecha Break",
        period="Mar 2024 to Jul 2025",
        detail=(
            "185,000 members. My job was turning a firehose of player reports into "
            "something the developers could act on."
        ),
    ),
)


CREDENTIALS = (
    "I took first place at HackMe 2024, solving their problem statement in C++, and "
    "completed the JPMorgan Chase software engineering simulation in 2026."
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


def all_repo_urls() -> set[str]:
    """Every GitHub repository URL the README is allowed to point at."""
    urls = {p.url for p in PROJECTS}
    urls.update(EXTRA_REPOS.values())
    urls.add(f"https://github.com/{USERNAME}/{USERNAME}")
    return urls
