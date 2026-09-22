# Azrah design direction

## Principles

1. **System colors remain authoritative.** Use KDE palette roles and the active color scheme instead of embedding a fixed light or dark palette.
2. **Geometry is square and deliberate.** Default controls and window frames avoid decorative rounding; spacing and alignment keep the result calm rather than cramped.
3. **Interaction is two-tone.** Selection, focus, hover, and active states normally use a base surface plus one system accent/contrast tone, without extra gradients or ornamental layers.
4. **Borders carry structure.** Prefer crisp one-pixel separators and outlines where Breeze relies on soft shape or depth. Preserve legibility at fractional scale factors.
5. **Restraint beats novelty.** Animation, shadow, and highlight changes clarify state without competing with application content.
6. **Accessibility is a constraint.** Focus remains obvious, disabled controls distinguishable, and text/icon contrast usable across light, dark, high-contrast, and custom KDE color schemes.

“Omarchy-like” describes the desired visual character, not a fixed color palette or a requirement to copy another project's assets.

## First visual milestone

1. Define shared corner-radius, border-width, and highlight metrics.
2. Square buttons, fields, menus, tabs, item views, scrollbars, and progress controls.
3. Establish two-tone hover/focus/selection treatment using KDE palette roles.
4. Apply the geometry and active/inactive language to the KWin decoration.
5. Audit shadows, animations, high-DPI rendering, and non-default color schemes.

Color schemes, cursors, wallpapers, Plasma shell themes, icons, GTK styling, and mobile-specific QQC2 themes are outside this milestone.

## Decision log

Each stable decision should state the date, affected components, decision, color roles or metrics used, alternatives rejected, and screenshot/test conditions.

### 2026-09-21 — Fork identity and compatibility

- Public name: **Azrah**.
- Install model: side-by-side with stock Breeze.
- Primary scope: Qt 6 widget style and KWin decoration.
- Internal Breeze source names and namespaces remain where they do not leak into installed identity, preserving a practical path for upstream fixes.
- Inherited Breeze colors, cursors, wallpapers, translations, and utilities are disabled until they receive distinct Azrah identities and a design review.

### 2026-09-21 — Boxy focus-frame decoration

- Window geometry is square by default; Breeze-style rounding remains an explicit option and applies consistently to the frame, titlebar, outline, and shadow.
- Titlebars are hidden by default for a tiling-window-manager character, but remain globally configurable and overridable through Breeze-compatible per-window exceptions.
- Active windows use a one-pixel KDE system-highlight outline. Inactive windows retain a one-pixel neutral system-derived outline.
- Maximized windows omit the outline at screen edges. Shadows, invisible resize margins, and user-selected border sizes remain supported.

### 2026-09-21 — Border-size-aware outlines

- By default, the visible outline follows KDE's effective Window Border Size, including per-window overrides. `None` and `No Sides` therefore omit the outline.
- Azrah recommends KDE's `Normal` border size so a visible, deliberate frame is the default while the user's global choice remains authoritative.
- An optional 1–32 logical-pixel override controls the outline width.
- Disabled outlines and maximized windows remain outline-free regardless of the width override.

### 2026-09-22 — Inset frame geometry

- The outline is painted inside the decoration margins, so its full width is included in the window geometry used by tiling layouts and does not consume surrounding gaps.
- A manual width override reserves at least the same DPI-scaled decoration margin. It does not change the configured KDE or per-window border-size value.
- Square mode uses rectangular, non-antialiased frame and shadow masks. Rounded painting remains available only through the explicit Rounded Corners option.
