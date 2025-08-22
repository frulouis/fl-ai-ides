"""
CLI for AI IDEs & Coding Agents catalog.
- list: show catalog entries
- add: append a new entry to YAML
- generate: create docs/AI_IDEs.md from YAML
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table
from jinja2 import Template

app = typer.Typer(help="Manage the AI IDEs & Agents catalog")
console = Console()

# Default paths
ROOT = Path(__file__).resolve().parents[1]
CONFIGS = ROOT / "configs"
DOCS = ROOT / "docs"
CATALOG = CONFIGS / "ai_ides.yaml"
OUTPUT_MD = DOCS / "AI_IDEs.md"


def load_catalog(path: Path = CATALOG) -> dict:
    """Load YAML catalog into a dict."""
    if not path.exists():
        typer.secho(f"Catalog not found: {path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"items": []}


def save_catalog(data: dict, path: Path = CATALOG) -> None:
    """Persist catalog YAML with sorted keys for stability."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


@app.command()
def list() -> None:  # noqa: A003 - intentional name for CLI
    """List catalog entries in a table."""
    data = load_catalog()
    items = data.get("items", [])

    table = Table(title="AI IDEs & Coding Agents", show_lines=False)
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("URL", style="blue")
    table.add_column("Category", style="magenta")

    for idx, item in enumerate(items, start=1):
        table.add_row(str(idx), item.get("name", ""), item.get("url", ""), item.get("category", ""))

    console.print(table)


@app.command()
def add(
    name: str = typer.Option(..., help="Tool name"),
    url: str = typer.Option(..., help="Homepage URL"),
    category: Optional[str] = typer.Option(None, help="Optional category"),
    notes: Optional[str] = typer.Option(None, help="Optional notes"),
) -> None:
    """Append a new entry to the catalog YAML."""
    data = load_catalog()
    items = data.setdefault("items", [])

    # Prevent duplicate names
    if any(i.get("name", "").strip().lower() == name.strip().lower() for i in items):
        typer.secho("Entry with that name already exists.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=2)

    entry = {"name": name, "url": url}
    if category:
        entry["category"] = category
    if notes:
        entry["notes"] = notes

    items.append(entry)
    save_catalog(data)
    typer.secho(f"Added: {name}", fg=typer.colors.GREEN)


DOC_TEMPLATE = Template(
    """
# AI IDEs and AI Coding Agents

{% for item in items -%}
{{ loop.index }}. [{{ item.name }}]({{ item.url }}){% if item.category %} — {{ item.category }}{% endif %}{% if item.notes %} — {{ item.notes }}{% endif %}
{% endfor %}
""".strip()
)


@app.command()
def generate() -> None:
    """Generate docs/AI_IDEs.md from YAML catalog."""
    data = load_catalog()
    items = data.get("items", [])

    # Pass dictionaries directly; Jinja2 allows attribute-like access to dict keys
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    rendered = DOC_TEMPLATE.render(items=items)
    OUTPUT_MD.write_text(rendered + "\n", encoding="utf-8")
    typer.secho(f"Generated: {OUTPUT_MD}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
