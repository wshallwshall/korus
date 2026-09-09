#!/usr/bin/env python3
"""Rebuild G13 from TOKEN-ACCOUNTING.md. Requires matplotlib (tested with 3.11.1)."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
COLUMNS = ("Account", "Weekly meter", "Tokens in window", "Non-cache-read",
           "Raw per 1 percent", "Non-cache-read per 1 percent")


@dataclass(frozen=True)
class Measurement:
    date: str
    accounts: tuple[str, ...]
    raw: tuple[int, ...]
    non_cache: tuple[int, ...]


def parse_measurement(source: str) -> Measurement:
    """Reject missing, duplicate, malformed, or ambiguous source rows and headers."""
    lines = source.splitlines()
    headers = [i for i, line in enumerate(lines)
               if line.startswith("|") and "Raw per 1 percent" in line]
    if len(headers) != 1:
        raise ValueError("Expected exactly one token measurement table")
    start = headers[0]
    split = lambda line: tuple(part.strip() for part in line.strip().strip("|").split("|"))
    if split(lines[start]) != COLUMNS:
        raise ValueError("Unexpected token measurement columns")
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        row = split(line)
        if len(row) != len(COLUMNS):
            raise ValueError("Wrong measurement row width")
        if not re.fullmatch(r"(?:[1-9][0-9]?|100) percent", row[1]):
            raise ValueError("Invalid weekly meter")
        if any(not re.fullmatch(r"[1-9][0-9]{0,2}(?:,[0-9]{3})*", v) for v in row[2:]):
            raise ValueError("Invalid token count")
        rows.append(row)
    if tuple(row[0] for row in rows) != ("A", "B", "C", "D"):
        raise ValueError("Expected exactly accounts A, B, C, D, in order")
    dates = re.findall(r"^Four accounts measured on (\d{4}-\d{2}-\d{2})", source, re.MULTILINE)
    if len(dates) != 1:
        raise ValueError("Missing or ambiguous measurement date")
    if "activity on two days with no local transcripts" not in source:
        raise ValueError("Missing account D coverage caveat; review the chart annotation")
    return Measurement(dates[0], tuple(row[0] for row in rows),
                       tuple(int(row[4].replace(",", "")) for row in rows),
                       tuple(int(row[5].replace(",", "")) for row in rows))


def render_chart(data: Measurement, mobile: bool = False) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16,
                               "svg.fonttype": "none", "svg.hashsalt": "korus-g13",
                               "axes.unicode_minus": False})
    width, height = (320, 960) if mobile else (800, 490)
    fig = plt.figure(figsize=(width / 72, height / 72), facecolor="white")
    fig.text(.035, .97, "Four accounts,\ntwo token measures" if mobile else
             "Four accounts, two token measures", va="top", color="#242424", fontsize=20)
    fig.text(.035, .895 if mobile else .89, f"{data.date} | n = {len(data.accounts)} accounts",
             va="top", color="#424242", fontsize=16)
    specs = [(data.raw, "Raw tokens", [0, 30_000_000, 60_000_000], ["0", "30m", "60m"]),
             (data.non_cache, "Non-cache-read tokens", [0, 800_000, 1_600_000], ["0", "0.8m", "1.6m"])]
    for index, (values, title, ticks, labels) in enumerate(specs):
        bounds = ([.17, .535 if index == 0 else .16, .77, .255] if mobile else
                  [.07 + index * .49, .24, .385, .52])
        ax = fig.add_axes(bounds)
        ax.set_title(title, loc="left", fontsize=16, pad=24, color="#242424")
        positions = [3, 2, 1, 0]
        bars = ax.barh(positions, values, height=.35, color="#0f6cbd", zorder=3)
        bars[-1].set_facecolor("#fff4ce")
        bars[-1].set_edgecolor("#835b00")
        bars[-1].set_hatch("///")
        for y, value in zip(positions, values):
            ax.text(0, y + .25, f"{value:,}", fontsize=16, color="#242424", va="bottom")
        ax.set_yticks(positions, ["A", "B", "C", "D*"])
        ax.set_xticks(ticks, labels)
        ax.set_xlim(0, max(ticks[-1], max(values)) * 1.06)
        ax.set_ylim(-.5, 3.8)
        ax.set_xlabel("Tokens per meter point", fontsize=16, labelpad=10)
        ax.grid(axis="x", color="#d1d1d1", zorder=0)
        ax.tick_params(axis="both", labelsize=16, colors="#424242")
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#424242")
    foot = ("* D lacks local transcripts\nfor two days of meter activity.\n"
            "1 point = 1% of weekly meter.\nToken use does not measure progress." if mobile else
            "* D lacks local transcripts for two days of meter activity.\n"
            "1 point = 1% of weekly meter. Token use does not measure progress.")
    fig.text(.035, .10 if mobile else .095, foot, va="top", fontsize=16, color="#424242", linespacing=1.45)
    output = StringIO()
    fig.savefig(output, format="svg", metadata={"Date": None, "Creator": "KORUS plot_token_meter.py"})
    plt.close(fig)
    svg = output.getvalue().replace(f'width="{width}pt" height="{height}pt"',
                                    f'width="{width}px" height="{height}px"')
    # Matplotlib bundles DejaVu Sans; browsers need their own local fallback.
    svg = svg.replace("font-family: 'DejaVu Sans'", "font-family: Arial, sans-serif")
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "docs/TOKEN-ACCOUNTING.md")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs/assets/charts")
    parser.add_argument("--check", action="store_true", help="Fail if committed exports differ")
    args = parser.parse_args()
    data = parse_measurement(args.source.read_text(encoding="utf-8"))
    for mobile in (False, True):
        path = args.output_dir / ("g13-token-meter-mobile.svg" if mobile else "g13-token-meter.svg")
        content = render_chart(data, mobile)
        if args.check:
            if not path.exists() or path.read_text(encoding="ascii") != content:
                print(f"Chart differs: {path}", file=sys.stderr)
                return 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="ascii", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
