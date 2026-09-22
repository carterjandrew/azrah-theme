# Azrah development log

This log records development incidents and implementation findings that should influence future work. Stable visual decisions belong in `design.md`.

## 2026-09-21 — User-local plugins installed but not discovered

### Symptoms

- `./scripts/dev install` completed successfully.
- Azrah did not appear in Application Style or Window Decorations after restarting Plasma.
- The restarted session felt temporarily slow, so the development installation was removed before further visual work.

### Cause

The helper hardcoded `~/.local/lib/qt6/plugins` into `QT_PLUGIN_PATH`. KDE's CMake install directories resolved the plugin root to `~/.local/lib/plugins` on the development system. The Azrah binaries were valid and their explicit KCM smoke tests passed when launched with the actual directory, but Plasma could not discover them through the configured path.

No log evidence showed Azrah loading into the slow session. KWin reported a temporary main-thread hang during startup, so the slowdown could not be attributed to Azrah itself.

### Resolution

- Uninstall Azrah and restart Plasma to verify a normal baseline.
- Derive the plugin root from the generated CMake install manifest by locating the installed `styles/azrah6.so`; never infer it from the distribution or Qt version.
- Write that resolved directory to the user environment file and print it after installation for verification.

### Development rule

Test a fresh build in a single application with an explicit `QT_PLUGIN_PATH` and `QT_STYLE_OVERRIDE=Azrah` before exposing it to the entire Plasma session. Do not restart or replace KWin automatically from development tooling.

## 2026-09-21 — First Azrah decoration identity

The initial visual change keeps Breeze's decoration implementation instead of replacing it with a border-only plugin. This preserves captions, buttons, shadows, resizing, shading, border-size support, and per-window exceptions while allowing Azrah to default to a titlebar-free workflow.

Corner radius is treated as a single geometry decision across painting, compositor metadata, outlines, and shadow masks. Active focus is communicated through the window palette's highlight color, so the frame follows KDE color schemes without a separate Azrah color setting.

## 2026-09-21 — Outline width and resize-border semantics

The decoration outline now derives its automatic thickness from the effective side-border calculation rather than a fixed one-pixel value. Reusing `borderSize(false, scale)` is important: it preserves KWin's global border size, Azrah's per-window exception mask, fractional scaling, and the zero-width meaning of both `None` and `No Sides`.

The manual outline-width setting initially changed only `KDecoration3::BorderOutline`; layout margins and invisible resize-only borders continued to follow KWin. Values were stored as logical pixels and snapped to the output scale when painted.

## 2026-09-22 — External outlines consumed tiling gaps

### Symptoms

- Thick outlines expanded beyond the geometry assigned to windows by a tiling layout, consuming part of the intended gap.
- Larger outlines exposed subtly rounded corners even when Azrah's Rounded Corners option was disabled.

### Cause

`KDecoration3::BorderOutline` is compositor-owned and rendered outside the decorated window. Its pixels are not part of the decoration margins reported to tiling layouts, and its rendering path is separate from Azrah's square frame painting.

### Resolution

Azrah now keeps the compositor outline empty and paints the focus border into real decoration margins. Automatic width reuses the effective KDE side-border size. A manual override reserves at least its DPI-scaled width in the decoration geometry, so its full painted area is included in tiling calculations. Square mode uses non-antialiased rectangular fills and a rectangular shadow cutout; only the explicit Rounded Corners option enables curved paths.
