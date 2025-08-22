"""
CLI for AI IDEs & Coding Agents catalog.
- list: show catalog entries
- add: append a new entry to YAML
- generate: inject the list into README only
"""
from __future__ import annotations

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
CATALOG = CONFIGS / "ai_ides.yaml"
README = ROOT / "README.md"


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


README_SECTION_TEMPLATE = Template(
    """
{% for item in items -%}
{{ loop.index }}. [{{ item.name }}]({{ item.url }}){% if item.category %} — {{ item.category }}{% endif %}{% if item.notes %} — {{ item.notes }}{% endif %}
{% endfor %}
""".strip()
)


@app.command()
def generate() -> None:
    """Inject the list into README between markers only."""
    data = load_catalog()
    items = data.get("items", [])

    if not README.exists():
        typer.secho("README.md not found; cannot inject", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    content = README.read_text(encoding="utf-8")
    start = "<!-- BEGIN: AI_IDE_LIST -->"
    end = "<!-- END: AI_IDE_LIST -->"
    if start in content and end in content and content.index(start) < content.index(end):
        pre = content.split(start)[0]
        post = content.split(end)[1]
        section = README_SECTION_TEMPLATE.render(items=items)
        new_content = f"{pre}{start}\n{section}\n{end}{post}"
        README.write_text(new_content, encoding="utf-8")
        typer.secho("Injected list into README.md", fg=typer.colors.GREEN)
    else:
        typer.secho("Markers not found in README; no changes made", fg=typer.colors.YELLOW)


if __name__ == "__main__":
    app()
