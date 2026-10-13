#!/usr/bin/env python3
"""Generate the small SVG contract used by the Azrah Plasma theme.

The element names follow KDE's Breeze Plasma theme so Plasma components can
consume Azrah as a partial theme and fall back to Breeze for everything else.
SPDX-License-Identifier: GPL-2.0-or-later
"""

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

PALETTE = {
    "Background": "#eff0f1",
    "Text": "#232629",
    "ButtonBackground": "#eff0f1",
    "ButtonText": "#232629",
    "ViewBackground": "#fcfcfc",
    "ViewText": "#232629",
    "Highlight": "#3daee9",
    "HighlightedText": "#ffffff",
    "ViewHover": "#93cee9",
    "ViewFocus": "#3daee9",
    "ComplementaryBackground": "#31363b",
    "ComplementaryText": "#eff0f1",
}


class Svg:
    def __init__(self, width: int = 1024, height: int = 1024) -> None:
        self.root = ET.Element(
            f"{{{SVG}}}svg",
            {"width": str(width), "height": str(height), "viewBox": f"0 0 {width} {height}"},
        )
        defs = ET.SubElement(self.root, f"{{{SVG}}}defs")
        css = "\n".join(f".ColorScheme-{name} {{ color: {color}; }}" for name, color in PALETTE.items())
        ET.SubElement(defs, f"{{{SVG}}}style", {"id": "current-color-scheme", "type": "text/css"}).text = css
        self.x = 4
        self.y = 4

    def next_row(self, height: int = 36) -> None:
        self.x = 4
        self.y += height

    def rect(
        self,
        element_id: str,
        width: float,
        height: float,
        color: str = "Background",
        opacity: float = 1.0,
        x: float | None = None,
        y: float | None = None,
    ) -> ET.Element:
        x = self.x if x is None else x
        y = self.y if y is None else y
        attrs = {
            "id": element_id,
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "class": f"ColorScheme-{color}",
            "fill": "currentColor",
        }
        if opacity != 1.0:
            attrs["fill-opacity"] = str(opacity)
        node = ET.SubElement(self.root, f"{{{SVG}}}rect", attrs)
        self.x = x + width + 4
        return node

    def circle(self, element_id: str, diameter: int, color: str, opacity: float = 1.0) -> None:
        attrs = {
            "id": element_id,
            "cx": str(self.x + diameter / 2),
            "cy": str(self.y + diameter / 2),
            "r": str(diameter / 2),
            "class": f"ColorScheme-{color}",
            "fill": "currentColor",
        }
        if opacity != 1.0:
            attrs["fill-opacity"] = str(opacity)
        ET.SubElement(self.root, f"{{{SVG}}}circle", attrs)
        self.x += diameter + 4

    def hint(self, element_id: str, width: float, height: float) -> None:
        self.rect(element_id, width, height, "Background", 0.0)

    def frame(self, prefix: str, border: int, fill: str, edge: str, opacity: float = 1.0) -> None:
        stem = f"{prefix}-" if prefix else ""
        # Separate source tiles; Plasma assembles these into a square nine-slice frame.
        self.rect(stem + "topleft", border, border, edge)
        self.rect(stem + "top", 16, border, edge)
        self.rect(stem + "topright", border, border, edge)
        self.next_row(max(border, 2) + 4)
        self.rect(stem + "left", border, 16, edge)
        self.rect(stem + "center", 16, 16, fill, opacity)
        self.rect(stem + "right", border, 16, edge)
        self.next_row(20)
        self.rect(stem + "bottomleft", border, border, edge)
        self.rect(stem + "bottom", 16, border, edge)
        self.rect(stem + "bottomright", border, border, edge)
        self.next_row(max(border, 2) + 4)

    def margins(self, prefix: str, size: int) -> None:
        stem = f"{prefix}-" if prefix else ""
        self.hint(stem + "hint-top-margin", 1, size)
        self.hint(stem + "hint-bottom-margin", 1, size)
        self.hint(stem + "hint-left-margin", size, 1)
        self.hint(stem + "hint-right-margin", size, 1)
        self.next_row(max(size, 2) + 4)

    def insets(self, prefix: str, size: int) -> None:
        stem = f"{prefix}-" if prefix else ""
        self.hint(stem + "hint-top-inset", 1, size)
        self.hint(stem + "hint-bottom-inset", 1, size)
        self.hint(stem + "hint-left-inset", size, 1)
        self.hint(stem + "hint-right-inset", size, 1)
        self.next_row(max(size, 2) + 4)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.root, space="  ")
        ET.ElementTree(self.root).write(path, encoding="utf-8", xml_declaration=True)


def popup(path: Path, border: int, opacity: float) -> None:
    svg = Svg()
    svg.hint("hint-stretch-borders", 1, 1)
    svg.next_row()
    svg.frame("", border, "Background", "Highlight", opacity)
    svg.margins("", border)
    svg.insets("", border)
    svg.write(path)


def tooltip(path: Path) -> None:
    svg = Svg()
    svg.hint("hint-tile-center", 1, 1)
    svg.next_row()
    svg.frame("", 1, "Background", "Highlight", 0.94)
    svg.margins("", 6)
    svg.insets("", 1)
    svg.write(path)


def framed_states(path: Path, states: list[tuple[str, str, str, float]], margin: int = 5) -> None:
    svg = Svg()
    svg.hint("hint-tile-center", 1, 1)
    svg.next_row()
    for prefix, fill, edge, opacity in states:
        svg.frame(prefix, 1, fill, edge, opacity)
        svg.margins(prefix, margin)
    svg.write(path)


def button(path: Path) -> None:
    states = [
        ("normal", "ButtonBackground", "Text", 1.0),
        ("hover", "ButtonBackground", "Highlight", 1.0),
        ("focus", "ButtonBackground", "Highlight", 1.0),
        ("pressed", "Highlight", "Highlight", 1.0),
        ("toolbutton-hover", "ButtonBackground", "Highlight", 1.0),
        ("toolbutton-focus", "ButtonBackground", "Highlight", 1.0),
        ("toolbutton-pressed", "Highlight", "Highlight", 1.0),
    ]
    svg = Svg()
    for prefix, fill, edge, opacity in states:
        svg.frame(prefix, 1, fill, edge, opacity)
        svg.margins(prefix, 5)
    svg.hint("normal-hint-compose-over-border", 1, 1)
    svg.hint("pressed-hint-compose-over-border", 1, 1)
    svg.write(path)


def lineedit(path: Path) -> None:
    svg = Svg()
    svg.hint("hint-tile-center", 1, 1)
    svg.hint("hint-focus-over-base", 1, 1)
    svg.next_row()
    for prefix, fill, edge, opacity in [
        ("base", "ViewBackground", "Text", 1.0),
        ("hover", "ViewBackground", "Highlight", 1.0),
        ("focus", "ViewBackground", "Highlight", 1.0),
        ("focusframe", "ViewBackground", "Highlight", 0.0),
    ]:
        svg.frame(prefix, 1, fill, edge, opacity)
        svg.margins(prefix, 5)
    svg.write(path)


def listitem(path: Path) -> None:
    svg = Svg()
    svg.hint("hint-tile-center", 1, 1)
    svg.next_row()
    for state, fill, edge, opacity in [
        ("normal", "ViewBackground", "ViewBackground", 0.0),
        ("hover", "ViewHover", "Highlight", 0.35),
        ("pressed", "Highlight", "Highlight", 1.0),
        ("section", "ButtonBackground", "Text", 1.0),
    ]:
        svg.frame(state, 1, fill, edge, opacity)
        svg.margins(state, 2)
    svg.rect("separator", 20, 1, "Text", 0.35)
    svg.write(path)


def viewitem(path: Path) -> None:
    framed_states(path, [
        ("normal", "ViewBackground", "ViewBackground", 0.0),
        ("hover", "ViewHover", "Highlight", 0.35),
        ("selected", "Highlight", "Highlight", 1.0),
        ("selected+hover", "Highlight", "HighlightedText", 1.0),
    ], 2)


def tabbar(path: Path) -> None:
    framed_states(path, [
        (f"{direction}-active-tab", "ButtonBackground", "Highlight", 1.0)
        for direction in ("north", "south", "east", "west")
    ], 3)


def scrollbar(path: Path) -> None:
    states = [
        ("background-vertical", "ViewBackground", "ViewBackground", 0.45),
        ("background-horizontal", "ViewBackground", "ViewBackground", 0.45),
        ("slider", "Text", "Text", 0.55),
        ("mouseover-slider", "Highlight", "Highlight", 1.0),
    ]
    svg = Svg()
    svg.hint("hint-tile-center", 1, 1)
    svg.hint("private-hint-show-separator", 1, 1)
    svg.next_row()
    for state, fill, edge, opacity in states:
        svg.frame(state, 1, fill, edge, opacity)
        svg.insets(state, 1)
    svg.hint("hint-scrollbar-size", 12, 12)
    svg.write(path)


def slider(path: Path) -> None:
    svg = Svg()
    svg.hint("hint-tile-center", 1, 1)
    svg.hint("hint-handle-size", 16, 16)
    svg.next_row(20)
    for orientation in ("horizontal", "vertical"):
        svg.circle(f"{orientation}-slider-handle", 16, "Text")
        svg.circle(f"{orientation}-slider-hover", 16, "Highlight")
        svg.circle(f"{orientation}-slider-focus", 16, "Highlight")
        svg.circle(f"{orientation}-slider-shadow", 16, "Text", 0.0)
        svg.next_row(20)
    svg.write(path)


def switch(path: Path) -> None:
    svg = Svg()
    svg.hint("hint-stretch-borders", 1, 1)
    svg.hint("hint-bar-size", 32, 16)
    svg.next_row(20)
    for state, color, opacity in (("active", "Highlight", 1.0), ("inactive", "Text", 0.35)):
        svg.rect(f"{state}-left", 1, 16, color, opacity)
        svg.rect(f"{state}-center", 30, 16, color, opacity)
        svg.rect(f"{state}-right", 1, 16, color, opacity)
        svg.next_row(20)
    for state, color, opacity in (
        ("handle", "ButtonBackground", 1.0),
        ("handle-focus", "Highlight", 1.0),
        ("handle-hover", "Highlight", 1.0),
        ("handle-pressed", "HighlightedText", 1.0),
        ("handle-shadow", "Text", 0.0),
    ):
        svg.rect(state, 14, 14, color, opacity)
    svg.write(path)


def checkmarks(path: Path) -> None:
    svg = Svg(64, 32)
    checkbox = ET.SubElement(svg.root, f"{{{SVG}}}path", {
        "id": "checkbox", "d": "M 2,8 6,12 14,2", "fill": "none",
        "stroke": "currentColor", "stroke-width": "2", "class": "ColorScheme-HighlightedText",
    })
    checkbox.set("stroke-linecap", "square")
    svg.circle("radiobutton", 8, "HighlightedText")
    svg.write(path)


def radiobutton(path: Path) -> None:
    svg = Svg(160, 40)
    for state, color, opacity in (
        ("normal", "Text", 0.55),
        ("hover", "Highlight", 1.0),
        ("focus", "Highlight", 1.0),
        ("checked", "Highlight", 1.0),
        ("symbol", "HighlightedText", 1.0),
        ("shadow", "Text", 0.0),
    ):
        svg.circle(state, 16 if state != "symbol" else 8, color, opacity)
    svg.hint("hint-size", 16, 16)
    svg.write(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--popup-border-width", required=True, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 1 <= args.popup_border_width <= 32:
        raise SystemExit("popup border width must be from 1 to 32")
    widgets = args.output / "widgets"
    popup(widgets / "background.svg", args.popup_border_width, 0.94)
    popup(args.output / "solid/widgets/background.svg", args.popup_border_width, 1.0)
    popup(args.output / "translucent/widgets/background.svg", args.popup_border_width, 0.78)
    button(widgets / "button.svg")
    lineedit(widgets / "lineedit.svg")
    listitem(widgets / "listitem.svg")
    viewitem(widgets / "viewitem.svg")
    tabbar(widgets / "tabbar.svg")
    scrollbar(widgets / "scrollbar.svg")
    slider(widgets / "slider.svg")
    switch(widgets / "switch.svg")
    checkmarks(widgets / "checkmarks.svg")
    radiobutton(widgets / "radiobutton.svg")
    tooltip(widgets / "tooltip.svg")


if __name__ == "__main__":
    main()
