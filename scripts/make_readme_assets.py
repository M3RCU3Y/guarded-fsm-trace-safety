from __future__ import annotations

import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"

COLORS = {
    "ink": "#172033",
    "muted": "#64748b",
    "rule": "#d9e2ec",
    "panel": "#f8fafc",
    "blue": "#1f4e79",
    "green": "#1f7a5a",
    "red": "#8a3d2e",
    "purple": "#6b5b95",
    "gold": "#b7791f",
}

CONTROLLER_COLORS = {
    "No guard": COLORS["red"],
    "Schema guard": COLORS["purple"],
    "Finite-state guard": COLORS["green"],
}


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def write_svg(name: str, body: str, width: int, height: int) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
  <rect width="{width}" height="{height}" fill="white"/>
{body}
</svg>
"""
    (ASSETS / name).write_text(svg, encoding="utf-8")


def text(x: float, y: float, value: str, size: int = 14, fill: str = COLORS["ink"], weight: str = "400", anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(value)}</text>'


def line(x1: float, y1: float, x2: float, y2: float, stroke: str = COLORS["rule"], width: float = 1.0, dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"{dash_attr}/>'


def rounded_rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = COLORS["rule"], r: int = 10, sw: float = 1.0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def arrow(x1: float, y1: float, x2: float, y2: float, stroke: str = COLORS["blue"], width: float = 2.0) -> str:
    marker = '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="' + stroke + '"/></marker>'
    return marker + f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}" marker-end="url(#arrow)"/>'


def load_rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def polyline(points: list[tuple[float, float]], color: str) -> str:
    values = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    circles = "\n".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{color}" stroke="white" stroke-width="1.3"/>' for x, y in points)
    return f'<polyline points="{values}" fill="none" stroke="{color}" stroke-width="2.3" stroke-linejoin="round" stroke-linecap="round"/>\n{circles}'


def line_chart(name: str, title: str, subtitle: str, rows: list[dict[str, str]], metric: str, y_label: str) -> None:
    width, height = 920, 470
    left, right, top, bottom = 82, 32, 78, 82
    plot_w = width - left - right
    plot_h = height - top - bottom

    controllers = ["No guard", "Schema guard", "Finite-state guard"]
    max_y = max(float(row[metric]) for row in rows)
    max_y = max(0.5, max_y)

    def sx(alpha: float) -> float:
        return left + alpha * plot_w

    def sy(value: float) -> float:
        return top + plot_h - (value / max_y) * plot_h

    parts = [
        rounded_rect(0, 0, width, height, "white", "#e5edf5", 0),
        text(34, 38, title, 24, COLORS["ink"], "700"),
        text(34, 62, subtitle, 13, COLORS["muted"]),
        line(left, top, left, top + plot_h, "#9aa8b7", 1.2),
        line(left, top + plot_h, left + plot_w, top + plot_h, "#9aa8b7", 1.2),
    ]

    for i in range(6):
        value = max_y * i / 5
        y = sy(value)
        parts.append(line(left, y, left + plot_w, y, COLORS["rule"], 0.9))
        parts.append(text(left - 12, y + 4, f"{value:.2f}", 11, COLORS["muted"], anchor="end"))

    for i in range(0, 11, 2):
        x = sx(i / 10)
        parts.append(line(x, top + plot_h, x, top + plot_h + 5, "#9aa8b7", 1))
        parts.append(text(x, top + plot_h + 24, f"{i/10:.1f}", 11, COLORS["muted"], anchor="middle"))

    for controller in controllers:
        points = []
        controller_rows = [row for row in rows if row["controller"] == controller]
        controller_rows.sort(key=lambda row: float(row["alpha"]))
        for row in controller_rows:
            points.append((sx(float(row["alpha"])), sy(float(row[metric]))))
        parts.append(polyline(points, CONTROLLER_COLORS[controller]))

    parts.append(text(left + plot_w / 2, height - 24, "proposal noise alpha", 12, COLORS["muted"], anchor="middle"))
    parts.append(text(24, top + plot_h / 2, y_label, 12, COLORS["muted"], anchor="middle"))

    legend_x, legend_y = width - 278, 32
    parts.append(rounded_rect(legend_x, legend_y, 242, 82, "white", COLORS["rule"], 8))
    for idx, controller in enumerate(controllers):
        y = legend_y + 24 + idx * 20
        parts.append(line(legend_x + 16, y - 4, legend_x + 44, y - 4, CONTROLLER_COLORS[controller], 2.5))
        parts.append(text(legend_x + 54, y, controller, 12, COLORS["ink"]))

    write_svg(name, "\n".join(parts), width, height)


def architecture() -> None:
    width, height = 980, 330
    parts = [
        text(34, 42, "Runtime boundary", 26, COLORS["ink"], "700"),
        text(34, 68, "The model proposes actions. Only guard-accepted actions reach tools.", 14, COLORS["muted"]),
    ]
    boxes = [
        (44, 126, 155, 72, "Proposal source", "untrusted"),
        (250, 126, 140, 72, "Parser", "finite action"),
        (440, 110, 180, 104, "FSM guard", "state + policy table"),
        (674, 126, 140, 72, "Accepted trace", "auditable"),
        (858, 126, 86, 72, "Tools", "effects"),
    ]
    for x, y, w, h, title, sub in boxes:
        parts.append(rounded_rect(x, y, w, h, "white", COLORS["rule"], 12, 1.2))
        parts.append(text(x + w / 2, y + 32, title, 15, COLORS["ink"], "700", "middle"))
        parts.append(text(x + w / 2, y + 54, sub, 12, COLORS["muted"], "400", "middle"))
    for x1, x2 in [(199, 250), (390, 440), (620, 674), (814, 858)]:
        parts.append(arrow(x1, 162, x2, 162, COLORS["blue"], 2.2))
    parts.append(line(530, 214, 530, 266, COLORS["red"], 2, "5 4"))
    parts.append(rounded_rect(416, 264, 228, 42, "#fff7f5", "#f0c7bd", 9))
    parts.append(text(530, 290, "rejected proposals are suppressed", 13, COLORS["red"], "600", "middle"))
    write_svg("architecture.svg", "\n".join(parts), width, height)


def fsm_diagram(name: str, title: str, nodes: list[tuple[str, float, float]], edges: list[tuple[str, str, str, str]]) -> None:
    width, height = 920, 340
    parts = [text(34, 42, title, 24, COLORS["ink"], "700")]
    positions = {label: (x, y) for label, x, y in nodes}
    for src, dst, label, color in edges:
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        parts.append(arrow(x1 + 70, y1, x2 - 70, y2, color, 2.1))
        parts.append(text((x1 + x2) / 2, (y1 + y2) / 2 - 10, label, 12, color, "600", "middle"))
    for label, x, y in nodes:
        parts.append(rounded_rect(x - 70, y - 30, 140, 60, "white", COLORS["rule"], 30, 1.4))
        parts.append(text(x, y + 5, label, 14, COLORS["ink"], "700", "middle"))
    write_svg(name, "\n".join(parts), width, height)


def enumeration_summary() -> None:
    rows = load_rows("guarded_fsm_enumeration_results.csv")
    width, height = 920, 380
    parts = [
        text(34, 42, "Bounded exhaustive enumeration", 24, COLORS["ink"], "700"),
        text(34, 66, "Unsafe accepted traces found across every proposal sequence up to the reported depth.", 13, COLORS["muted"]),
    ]
    final_rows = {}
    for row in rows:
        key = (row["policy"], row["controller"])
        if key not in final_rows or int(row["depth"]) > int(final_rows[key]["depth"]):
            final_rows[key] = row
    values = sorted(final_rows.values(), key=lambda row: (row["policy"], row["controller"]))
    max_unsafe = max(int(row["unsafe_sequences"]) for row in values)
    left, top = 84, 106
    bar_h, gap = 26, 16
    for idx, row in enumerate(values):
        y = top + idx * (bar_h + gap)
        unsafe = int(row["unsafe_sequences"])
        label = f"{row['policy']} / {row['controller']}"
        color = CONTROLLER_COLORS.get(row["controller"], COLORS["blue"])
        width_ratio = 0 if unsafe == 0 else unsafe / max_unsafe
        parts.append(text(left, y + 18, label, 12, COLORS["ink"]))
        parts.append(rounded_rect(300, y, 470, bar_h, "#eef3f8", "#e5edf5", 6))
        if unsafe:
            parts.append(rounded_rect(300, y, 470 * width_ratio, bar_h, color, color, 6))
        else:
            parts.append(rounded_rect(300, y, 10, bar_h, COLORS["green"], COLORS["green"], 6))
        parts.append(text(792, y + 18, f"{unsafe:,}", 13, COLORS["ink"], "700"))
    write_svg("enumeration_summary.svg", "\n".join(parts), width, height)


def test_matrix() -> None:
    width, height = 920, 300
    cards = [
        ("Artifact validation", "passed", "expected counts, metadata, split CSVs"),
        ("Unit tests", "7 passed", "guard behavior and enumeration checks"),
        ("FSM unsafe traces", "0", "approval depth 8, disclosure depth 6"),
    ]
    parts = [
        text(34, 42, "Verification snapshot", 24, COLORS["ink"], "700"),
        text(34, 66, "The checks are intentionally small enough to read and rerun.", 13, COLORS["muted"]),
    ]
    for i, (title, value, sub) in enumerate(cards):
        x = 44 + i * 292
        parts.append(rounded_rect(x, 112, 248, 118, "white", COLORS["rule"], 14, 1.2))
        parts.append(text(x + 22, 146, title, 14, COLORS["muted"], "600"))
        parts.append(text(x + 22, 182, value, 31, COLORS["green"], "800"))
        parts.append(text(x + 22, 210, sub, 12, COLORS["ink"]))
    write_svg("verification_snapshot.svg", "\n".join(parts), width, height)


def hero() -> None:
    width, height = 1100, 330
    parts = [
        '<defs><linearGradient id="hero" x1="0" x2="1" y1="0" y2="1"><stop offset="0%" stop-color="#102a43"/><stop offset="55%" stop-color="#1f4e79"/><stop offset="100%" stop-color="#1f7a5a"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="22" fill="url(#hero)"/>',
        text(54, 82, "Guarded finite-state mediation", 36, "white", "800"),
        text(56, 120, "A small runtime boundary for trace-safe tool actions", 18, "#dbeafe", "500"),
        '<rect x="58" y="172" width="216" height="56" rx="14" fill="#ffffff" fill-opacity="0.10" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1"/>',
        text(86, 207, "0 unsafe FSM traces", 18, "white", "800"),
        '<rect x="304" y="172" width="216" height="56" rx="14" fill="#ffffff" fill-opacity="0.10" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1"/>',
        text(332, 207, "standard library", 18, "white", "800"),
        '<rect x="550" y="172" width="248" height="56" rx="14" fill="#ffffff" fill-opacity="0.10" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1"/>',
        text(578, 207, "reproducible checks", 18, "white", "800"),
    ]
    write_svg("hero.svg", "\n".join(parts), width, height)


def main() -> None:
    hero()
    architecture()
    fsm_diagram(
        "approval_fsm.svg",
        "Approval-gated execution",
        [("Idle", 120, 185), ("NeedApproval", 335, 185), ("CanExecute", 560, 185), ("Terminal", 780, 185)],
        [
            ("Idle", "NeedApproval", "request", COLORS["blue"]),
            ("NeedApproval", "CanExecute", "approve", COLORS["green"]),
            ("CanExecute", "Terminal", "execute", COLORS["blue"]),
        ],
    )
    fsm_diagram(
        "disclosure_fsm.svg",
        "Disclosure guard",
        [("Clean", 150, 185), ("Private", 450, 185), ("Redacted", 750, 185)],
        [
            ("Clean", "Private", "readPrivate", COLORS["blue"]),
            ("Private", "Redacted", "redact", COLORS["green"]),
            ("Redacted", "Private", "readPrivate", COLORS["purple"]),
        ],
    )
    line_chart(
        "approval_unsafe.svg",
        "Approval policy: unsafe accepted traces",
        "Schema validity does not remember whether approval happened.",
        load_rows("guarded_fsm_sim_results.csv"),
        "unsafe_rate",
        "unsafe rate",
    )
    line_chart(
        "disclosure_unsafe.svg",
        "Disclosure policy: unsafe accepted traces",
        "The stateful guard blocks external sends while private data is live.",
        load_rows("guarded_fsm_disclosure_results.csv"),
        "unsafe_rate",
        "unsafe rate",
    )
    enumeration_summary()
    test_matrix()


if __name__ == "__main__":
    main()
