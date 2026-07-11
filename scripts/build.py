from __future__ import annotations

import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
ENTRIES_DIR = ROOT / "entries"
DOCS_DIR = ROOT / "docs"
DATA_PATH = DOCS_DIR / "data" / "advantage-list.json"
INDEX_PATH = DOCS_DIR / "index.html"
MARKDOWN_PATH = ROOT / "ADVANTAGE_LIST.md"

CLASSIFICATIONS = {
    "local_time_to_answer": "Local time-to-answer separation",
    "local_runtime_lower_bound": "Local runtime lower bound",
    "paper_aligned_local_separation": "Paper-aligned local separation",
    "diagnostic_only": "Diagnostic only",
}


class EntryError(ValueError):
    pass


def require(value: object, description: str) -> None:
    if value is None or value == "" or value == []:
        raise EntryError(f"Missing {description}")


def validate_entry(entry: dict, path: Path) -> None:
    required = (
        "schema_version", "id", "title", "short_title", "evidence_date",
        "summary", "scale", "quantum", "classical_baselines", "comparison",
        "official_sources", "implementation", "claim_boundary", "tags",
    )
    for key in required:
        require(entry.get(key), f"{path.name}:{key}")
    if entry["schema_version"] != 1:
        raise EntryError(f"{path.name}: unsupported schema_version")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["id"]):
        raise EntryError(f"{path.name}: invalid id {entry['id']!r}")
    try:
        date.fromisoformat(entry["evidence_date"])
    except ValueError as exc:
        raise EntryError(f"{path.name}: invalid evidence_date") from exc
    if entry["scale"]["qubits"] < 1:
        raise EntryError(f"{path.name}: qubits must be positive")
    timings = entry["quantum"].get("timings", [])
    if sum(bool(item.get("primary")) for item in timings) != 1:
        raise EntryError(f"{path.name}: exactly one quantum timing must be primary")
    for timing in timings:
        if timing.get("seconds", 0) <= 0:
            raise EntryError(f"{path.name}: quantum timings must be positive")
        require(timing.get("scope"), f"{path.name}:quantum timing scope")
    for baseline in entry["classical_baselines"]:
        if baseline.get("seconds") is not None and baseline["seconds"] <= 0:
            raise EntryError(f"{path.name}: classical timings must be positive or null")
        for key in ("method", "scope", "status"):
            require(baseline.get(key), f"{path.name}:classical baseline {key}")
    classification = entry["comparison"].get("classification")
    if classification not in CLASSIFICATIONS:
        raise EntryError(f"{path.name}: unknown classification {classification!r}")
    for source in entry["official_sources"]:
        if not source.get("url", "").startswith("https://"):
            raise EntryError(f"{path.name}: official source must use HTTPS")
    implementation = entry["implementation"]
    if not implementation.get("edukaizen_url", "").startswith("https://"):
        raise EntryError(f"{path.name}: Edukaizen URL must use HTTPS")
    if not entry["claim_boundary"]:
        raise EntryError(f"{path.name}: claim boundary is required")


def load_entries() -> list[dict]:
    entries = []
    ids = set()
    for path in sorted(ENTRIES_DIR.glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        validate_entry(entry, path)
        if entry["id"] in ids:
            raise EntryError(f"Duplicate entry id {entry['id']}")
        ids.add(entry["id"])
        entries.append(entry)
    if not entries:
        raise EntryError("No entries found")
    return sorted(entries, key=lambda item: (item["evidence_date"], item["id"]))


def primary_timing(entry: dict) -> dict:
    return next(item for item in entry["quantum"]["timings"] if item["primary"])


def scale_text(entry: dict) -> str:
    sites = entry["scale"]["sites"]
    suffix = f" / {sites} sites" if sites is not None else ""
    return f"{entry['scale']['qubits']} qubits{suffix}"


def seconds_text(value: float | None) -> str:
    if value is None:
        return "not available"
    return f"{value:,.6f}".rstrip("0").rstrip(".") + " s"


def render_markdown(entries: list[dict]) -> str:
    lines = [
        "# Pro Student Quantum Advantage List",
        "",
        "Generated from the validated files in `entries/`. The classification is",
        "conditional on each entry's declared resources and claim boundary.",
        "",
        "| Project | Scale | Primary quantum timing | Classification |",
        "|---|---:|---:|---|",
    ]
    for entry in entries:
        timing = primary_timing(entry)
        lines.append(
            f"| [{entry['short_title']}](entries/{entry['id']}.json) | "
            f"{scale_text(entry)} | {seconds_text(timing['seconds'])} | "
            f"{CLASSIFICATIONS[entry['comparison']['classification']]} |"
        )
    for entry in entries:
        lines.extend([
            "",
            f"## {entry['title']}",
            "",
            entry["summary"],
            "",
            f"**Comparison:** {entry['comparison']['headline']}",
            "",
            "**Official sources**",
            "",
        ])
        lines.extend(f"- [{source['label']}]({source['url']})" for source in entry["official_sources"])
        lines.extend(["", "**Implementation**", "", f"- [Edukaizen project]({entry['implementation']['edukaizen_url']})"])
        lines.extend(f"- [GitHub repository]({url})" for url in entry["implementation"]["github_repositories"])
        lines.extend(["", "**Claim boundary**", ""])
        lines.extend(f"- {item}" for item in entry["claim_boundary"])
    return "\n".join(lines) + "\n"


def link_list(items: list[dict]) -> str:
    return "".join(
        f'<li><a href="{html.escape(item["url"], quote=True)}">{html.escape(item["label"])}</a></li>'
        for item in items
    )


def render_entry(entry: dict) -> str:
    timing = primary_timing(entry)
    baselines = "".join(
        "<tr>"
        f"<td>{html.escape(item['method'])}</td>"
        f"<td>{html.escape(seconds_text(item['seconds']))}</td>"
        f"<td>{html.escape(item['status'])}</td>"
        "</tr>"
        for item in entry["classical_baselines"]
    )
    boundaries = "".join(f"<li>{html.escape(item)}</li>" for item in entry["claim_boundary"])
    repositories = "".join(
        f'<li><a href="{html.escape(url, quote=True)}">GitHub implementation</a></li>'
        for url in entry["implementation"]["github_repositories"]
    )
    return f"""
    <section class="entry" id="{html.escape(entry['id'])}">
      <p class="kicker">{html.escape(CLASSIFICATIONS[entry['comparison']['classification']])}</p>
      <h2>{html.escape(entry['title'])}</h2>
      <p class="summary">{html.escape(entry['summary'])}</p>
      <dl class="facts">
        <div><dt>Scale</dt><dd>{html.escape(scale_text(entry))}</dd></div>
        <div><dt>Backend</dt><dd>{html.escape(entry['quantum']['backend'])}</dd></div>
        <div><dt>Primary timing</dt><dd>{html.escape(seconds_text(timing['seconds']))}</dd></div>
        <div><dt>Timing scope</dt><dd>{html.escape(timing['scope'])}</dd></div>
      </dl>
      <p class="headline"><strong>Measured comparison.</strong> {html.escape(entry['comparison']['headline'])}</p>
      <h3>Classical baselines</h3>
      <div class="table-wrap"><table><thead><tr><th>Method</th><th>Wall time</th><th>Status</th></tr></thead><tbody>{baselines}</tbody></table></div>
      <div class="columns">
        <div><h3>Official sources</h3><ul>{link_list(entry['official_sources'])}</ul></div>
        <div><h3>Complete implementation</h3><ul><li><a href="{html.escape(entry['implementation']['edukaizen_url'], quote=True)}">Edukaizen project</a></li>{repositories}</ul></div>
      </div>
      <h3>Claim boundary</h3><ul>{boundaries}</ul>
      <p class="entry-data"><a href="https://github.com/BramDo/pro-student-quantum-advantage-list/blob/main/entries/{html.escape(entry['id'])}.json">View machine-readable entry</a></p>
    </section>"""


def render_html(entries: list[dict]) -> str:
    rows = "".join(
        "<tr>"
        f'<td><a href="#{html.escape(entry["id"])}">{html.escape(entry["short_title"])}</a></td>'
        f"<td>{html.escape(scale_text(entry))}</td>"
        f"<td>{html.escape(seconds_text(primary_timing(entry)['seconds']))}</td>"
        f"<td>{html.escape(CLASSIFICATIONS[entry['comparison']['classification']])}</td>"
        "</tr>"
        for entry in entries
    )
    sections = "".join(render_entry(entry) for entry in entries)
    updated = max(entry["evidence_date"] for entry in entries)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="An extensible register of student-scale local practical quantum advantage projects.">
  <title>Pro Student Quantum Advantage List</title>
  <style>
    :root {{ color-scheme: light; --ink:#14212b; --muted:#52616b; --line:#c7d1d7; --teal:#087f73; --orange:#dc5a32; --blue:#315f86; --paper:#ffffff; --wash:#f3f6f6; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--ink); background:var(--paper); }}
    a {{ color:#006f73; text-underline-offset:3px; }}
    header {{ border-top:8px solid var(--orange); padding:4rem 1.25rem 3rem; background:var(--wash); }}
    .wrap {{ max-width:1080px; margin:0 auto; }}
    h1 {{ max-width:850px; margin:0 0 1rem; font-family:Georgia,serif; font-size:clamp(2.4rem,7vw,5rem); line-height:1.02; letter-spacing:0; }}
    h2,h3 {{ letter-spacing:0; }}
    h2 {{ font-family:Georgia,serif; font-size:clamp(1.8rem,4vw,2.7rem); }}
    .lede {{ max-width:800px; color:var(--muted); font-size:1.2rem; line-height:1.65; }}
    nav {{ margin-top:1.5rem; display:flex; flex-wrap:wrap; gap:1rem 1.5rem; }}
    main {{ max-width:1080px; margin:0 auto; padding:0 1.25rem 4rem; }}
    .intro {{ padding:3rem 0; border-bottom:1px solid var(--line); }}
    .definition {{ border-left:5px solid var(--teal); padding:1rem 1.25rem; background:#edf7f5; line-height:1.65; }}
    .table-wrap {{ overflow-x:auto; }}
    table {{ width:100%; min-width:720px; border-collapse:collapse; }}
    th,td {{ padding:.8rem; border:1px solid var(--line); text-align:left; vertical-align:top; }}
    th {{ background:var(--ink); color:white; }}
    tbody tr:nth-child(even) {{ background:#f6f8f8; }}
    .entry {{ padding:3.5rem 0; border-top:5px solid var(--blue); }}
    .entry:nth-of-type(3n+1) {{ border-top-color:var(--orange); }}
    .entry:nth-of-type(3n+2) {{ border-top-color:var(--teal); }}
    .kicker {{ color:var(--muted); font-size:.82rem; font-weight:750; text-transform:uppercase; }}
    .summary {{ max-width:880px; font-size:1.08rem; line-height:1.7; }}
    .facts {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); border-top:1px solid var(--line); border-bottom:1px solid var(--line); }}
    .facts div {{ padding:1rem; }}
    dt {{ color:var(--muted); font-size:.82rem; font-weight:700; text-transform:uppercase; }}
    dd {{ margin:.35rem 0 0; line-height:1.5; }}
    .headline {{ border-left:4px solid var(--ink); padding:1rem 1.2rem; background:#f6f7f8; line-height:1.65; }}
    .columns {{ display:grid; grid-template-columns:1fr 1fr; gap:2rem; }}
    li {{ margin:.45rem 0; line-height:1.55; }}
    .figure {{ margin:2rem 0; }}
    .figure img {{ width:100%; height:auto; border:1px solid var(--line); }}
    .figure figcaption {{ color:var(--muted); line-height:1.5; margin-top:.5rem; }}
    footer {{ border-top:1px solid var(--line); padding:2rem 1.25rem; color:var(--muted); }}
    @media(max-width:700px) {{ .facts,.columns {{ grid-template-columns:1fr; }} header {{ padding-top:2.6rem; }} }}
  </style>
</head>
<body>
  <header><div class="wrap">
    <p class="kicker">Open benchmark register</p>
    <h1>Pro Student Quantum Advantage List</h1>
    <p class="lede">Complete, challengeable quantum projects from students, hobbyists, independent researchers, and small teams. Every entry links the official work to a hardware implementation, a classical competitor, and an explicit claim boundary.</p>
    <nav><a href="https://edukaizen.nl/pro-student-quantum-advantage-list/">Edukaizen article</a><a href="https://github.com/BramDo/pro-student-quantum-advantage-list">GitHub repository</a><a href="data/advantage-list.json">JSON feed</a><a href="https://github.com/BramDo/pro-student-quantum-advantage-list/issues">Submit a challenge</a></nav>
  </div></header>
  <main>
    <section class="intro">
      <h2>What counts here</h2>
      <div class="definition"><strong>Local practical advantage</strong> means that a measured quantum workflow reached a useful answer faster than a named classical workflow for the same stated task on the resources actually available to the project. It is not proof against every classical algorithm or supercomputer.</div>
      <p>A stronger classical result is not a problem for this list. It is a successful challenge. The entry and its classification should change when the evidence changes.</p>
      <div class="table-wrap"><table><thead><tr><th>Project</th><th>Scale</th><th>Primary quantum timing</th><th>Classification</th></tr></thead><tbody>{rows}</tbody></table></div>
      <figure class="figure"><img src="assets/fermi-hubbard-120q-charge-density.png" alt="Measured charge-density outcome by site for the 120-qubit Fermi-Hubbard hardware run"><figcaption>One of the measured outcomes behind the list: the 120-qubit Fermi-Hubbard charge-density profile. The sector-plus-readout route is diagnostic because postselection discarded 98.9 percent of shots.</figcaption></figure>
    </section>
    {sections}
    <section class="intro"><h2>Make the list better</h2><p>Copy the entry template, add the official source and full implementation, state both timing scopes, and preserve every convergence or accuracy limitation. Classical challenges are first-class contributions.</p><p><a href="https://github.com/BramDo/pro-student-quantum-advantage-list/blob/main/CONTRIBUTING.md">Read the contribution guide</a>.</p></section>
  </main>
  <footer><div class="wrap">Evidence updated through {html.escape(updated)}. Content: CC BY 4.0. Code: MIT.</div></footer>
</body>
</html>
"""


def data_feed(entries: list[dict]) -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "project": "Pro Student Quantum Advantage List",
            "canonical_url": "https://edukaizen.nl/pro-student-quantum-advantage-list/",
            "repository": "https://github.com/BramDo/pro-student-quantum-advantage-list",
            "entry_count": len(entries),
            "entries": entries,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def outputs(entries: list[dict]) -> dict[Path, str]:
    return {
        MARKDOWN_PATH: render_markdown(entries),
        DATA_PATH: data_feed(entries),
        INDEX_PATH: render_html(entries),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when generated files are stale")
    args = parser.parse_args()
    try:
        entries = load_entries()
    except (EntryError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"validation error: {exc}", file=sys.stderr)
        return 1
    generated = outputs(entries)
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, content in generated.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
        if stale:
            print("stale generated files: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"validated {len(entries)} entries; generated files are current")
        return 0
    for path, content in generated.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

