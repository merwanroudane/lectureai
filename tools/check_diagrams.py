"""
فحص سلامة الرسوم المتحرّكة قبل النشر.

Why this exists
---------------
When the HTML parser meets certain tags inside ``<svg>`` — ``<b>``, ``<i>``,
``<span>``, ``<code>``, ``<p>`` and friends — it treats them as a signal to
leave foreign content, which silently *closes the SVG element*. Everything
after that point is dropped from the drawing. Nothing throws, nothing warns:
the diagram just loses most of its shapes.

Inside an SVG ``<text>`` the correct element is ``<tspan>``.

This script walks every public diagram builder in ``lib/anim*.py``, renders it,
and fails on:

  1. breakout tags inside the generated SVG,
  2. a missing or malformed ``viewBox``,
  3. any ``<text x=...>`` placed outside the viewBox (it would be clipped).

Run it with:  python tools/check_diagrams.py
"""

from __future__ import annotations

import importlib
import inspect
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

BREAKOUT_TAGS = [
    "b", "i", "u", "em", "strong", "code", "span", "small", "sub", "sup",
    "br", "p", "big", "s", "var", "tt", "div", "li", "ul", "ol", "table",
]

MODULES = ["lib.anim", "lib.anim_extra", "lib.anim_terms", "lib.anim_flow", "lib.anim_types"]


def check_svg(name: str, svg: str) -> list[str]:
    problems: list[str] = []

    for tag in BREAKOUT_TAGS:
        if re.search(rf"<{tag}[ >/]", svg):
            problems.append(f"breakout tag <{tag}> inside SVG — use <tspan> instead")

    vb = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', svg)
    if not vb:
        problems.append("missing or malformed viewBox")
        return problems

    width, height = float(vb.group(1)), float(vb.group(2))
    for m in re.finditer(r'<text x="(-?\d+(?:\.\d+)?)" y="(-?\d+(?:\.\d+)?)"', svg):
        x, y = float(m.group(1)), float(m.group(2))
        if not (0 <= x <= width):
            problems.append(f"text x={x:.0f} outside viewBox width {width:.0f}")
        if not (0 <= y <= height):
            problems.append(f"text y={y:.0f} outside viewBox height {height:.0f}")

    return problems


def main() -> int:
    failures = 0
    checked = 0

    for mod_name in MODULES:
        mod = importlib.import_module(mod_name)
        for fn_name, fn in vars(mod).items():
            if fn_name.startswith("_") or not inspect.isfunction(fn):
                continue
            if inspect.signature(fn).parameters or fn.__module__ != mod_name:
                continue
            try:
                svg = fn()
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL  {mod_name}.{fn_name}: raised {exc!r}")
                failures += 1
                continue
            if not isinstance(svg, str) or not svg.lstrip().startswith("<svg"):
                continue

            checked += 1
            seen: set[str] = set()
            for problem in check_svg(fn_name, svg):
                if problem in seen:
                    continue
                seen.add(problem)
                print(f"FAIL  {mod_name}.{fn_name}: {problem}")
                failures += 1

    print(f"\nchecked {checked} diagrams — {failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
