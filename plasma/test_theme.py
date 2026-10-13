#!/usr/bin/env python3
"""Contract checks for generated Azrah Plasma theme assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


REQUIRED = {
    "widgets/background.svg": {"center", "top", "right", "bottom", "left", "topleft", "topright", "bottomleft", "bottomright"},
    "widgets/button.svg": {"normal-center", "hover-center", "focus-center", "pressed-center"},
    "widgets/lineedit.svg": {"base-center", "hover-center", "focus-center"},
    "widgets/listitem.svg": {"normal-center", "hover-center", "pressed-center", "section-center"},
    "widgets/viewitem.svg": {"normal-center", "hover-center", "selected-center", "selected+hover-center"},
    "widgets/tabbar.svg": {"north-active-tab-center", "south-active-tab-center", "east-active-tab-center", "west-active-tab-center"},
    "widgets/scrollbar.svg": {"slider-center", "mouseover-slider-center", "hint-scrollbar-size"},
    "widgets/slider.svg": {"horizontal-slider-handle", "vertical-slider-handle", "hint-handle-size"},
    "widgets/switch.svg": {"active-center", "inactive-center", "handle", "hint-bar-size"},
    "widgets/checkmarks.svg": {"checkbox", "radiobutton"},
    "widgets/radiobutton.svg": {"checked", "focus", "hover", "normal", "symbol", "hint-size"},
    "widgets/tooltip.svg": {"center", "top", "right", "bottom", "left"},
}


def ids_and_root(path: Path) -> tuple[set[str], ET.Element]:
    root = ET.parse(path).getroot()
    return {node.get("id") for node in root.iter() if node.get("id")}, root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", required=True, type=Path)
    parser.add_argument("--popup-border-width", required=True, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = json.loads((args.theme / "metadata.json").read_text())
    assert metadata["KPlugin"]["Id"] == "azrah"

    for relative, required in REQUIRED.items():
        ids, root = ids_and_root(args.theme / relative)
        missing = required - ids
        assert not missing, f"{relative} is missing {sorted(missing)}"
        assert "current-color-scheme" in ids, f"{relative} lacks dynamic KDE colors"
        for node in root.iter():
            assert node.get("rx") in (None, "0", "0.0"), f"rounded geometry in {relative}"
            assert node.get("ry") in (None, "0", "0.0"), f"rounded geometry in {relative}"

    variants = [
        args.theme / "widgets/background.svg",
        args.theme / "solid/widgets/background.svg",
        args.theme / "translucent/widgets/background.svg",
    ]
    opacities = []
    for path in variants:
        ids, root = ids_and_root(path)
        assert REQUIRED["widgets/background.svg"] <= ids
        top = next(node for node in root.iter() if node.get("id") == "top")
        assert float(top.get("height")) == args.popup_border_width
        center = next(node for node in root.iter() if node.get("id") == "center")
        opacities.append(float(center.get("fill-opacity", "1")))
    assert len(set(opacities)) == 3, "popup opacity variants must remain distinct"


if __name__ == "__main__":
    main()
