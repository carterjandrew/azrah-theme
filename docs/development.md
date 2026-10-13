# Developing Azrah

## Supported development target

The primary target is Plasma 6 on Linux with Qt 6. The default preset builds the Azrah Qt widget style, settings tools, KWin decoration, partial Plasma theme, and existing tests.

Qt 5, color schemes, cursor themes, wallpapers, translations, and Breeze compatibility utilities are off by default. They remain source material, but must not be installed under upstream Breeze names.

## Dependencies

Run `./scripts/dev doctor` first. It checks the core build tools and ECM without changing the system.

On Arch Linux, install the development dependencies with:

```sh
sudo pacman -S --needed extra-cmake-modules ninja qt6-base qt6-declarative \
  frameworkintegration kcolorscheme kconfig kcoreaddons kguiaddons ki18n \
  kiconthemes kcmutils kwindowsystem kdecoration
```

The exact minimum versions are kept in the top-level CMake configuration. On other distributions, install the equivalent Qt 6, KDE Frameworks 6, KDecoration 3, ECM, CMake, and Ninja development packages.

## Daily workflow

```sh
./scripts/dev configure   # configure build/dev
./scripts/dev build       # configure if needed, then compile
./scripts/dev test        # compile, then run CTest with failure output
./scripts/dev install     # install for the current user and refresh KDE metadata
./scripts/dev uninstall   # remove exactly the files in the install manifests
```

Set `AZRAH_INSTALL_PREFIX` before `configure` to use a prefix other than `~/.local`. The install helper derives the Qt plugin directory from CMake's install manifest; do not assume a distro-specific path such as `lib/qt6/plugins`. For a custom prefix, the helper prints the exact directory to add to `QT_PLUGIN_PATH`.

The first default-prefix install creates `~/.config/environment.d/azrah.conf`. A full logout/login is required for Plasma to inherit it. Uninstall removes that file and CMake-installed files, but deliberately leaves directories and user settings intact.

## Testing changes

After installing, use a small Qt/KDE application to check common controls before changing the whole desktop. Force the style for one process with:

```sh
QT_STYLE_OVERRIDE=Azrah systemsettings
```

Check light and dark system schemes. For widgets, cover normal, hovered, focused, pressed, checked, disabled, and destructive states. For decorations, check active/inactive, maximized and tiled windows, every border size, and high-DPI scaling.

Development scripts do not restart or replace KWin. After installing a decoration change, reselect Azrah or log out and back in. Keep Breeze available as the recovery style.

The companion Plasma theme is not selected automatically. After installing it, select **Azrah** under **System Settings → Colors & Themes → Plasma Style**, or apply it explicitly:

```sh
plasma-apply-desktoptheme azrah
```

Use `plasmoidviewer` or `plasmawindowed` for focused applet testing. Check system-tray popups with normal, solid, and translucent Plasma behavior; Azrah preserves those modes rather than forcing opacity. Switching back to Breeze is the recovery path and does not require uninstalling Azrah.

## Troubleshooting

- If configuration reports ECM missing, install `extra-cmake-modules` (it is missing on the original development machine at the time of writing).
- If Azrah is absent from Application Style, compare `QT_PLUGIN_PATH` with the “Qt plugin directory” printed by `./scripts/dev install`, then start a new login session.
- If metadata looks stale, run `kbuildsycoca6`. Use `plasma-apply-desktoptheme --list-themes` to confirm that Plasma discovers the `azrah` theme.
- If an application does not refresh after saving, restart it while investigating the Azrah D-Bus reload signal.
- If the desktop becomes difficult to use, choose Breeze again. `./scripts/dev uninstall` does not touch Breeze.

## Incorporating upstream Breeze

```sh
git remote add upstream https://invent.kde.org/plasma/breeze.git
git fetch upstream
```

This checkout may be shallow; use `git fetch --unshallow origin` if history is required before a rebase. Rebase or merge upstream in a dedicated branch, keep the public Azrah identity changes, and avoid broad internal `Breeze::` or filename renames. Then run the full workflow and inspect a staged install for accidental `org.kde.breeze`, `breezerc`, or Breeze plugin filenames.

## Build options

Direct CMake users may control `BUILD_QT5`, `BUILD_QT6`, `BUILD_STYLE`, `BUILD_COLORS`, `BUILD_CURSOR`, `BUILD_MISC`, `BUILD_WITH_QTQUICK`, `WITH_DECORATIONS`, `WITH_WALLPAPERS`, and `BUILD_PLASMA_THEME`.

`AZRAH_PLASMA_POPUP_BORDER_WIDTH` sets the outer applet-popup frame from 1–32 logical pixels and defaults to `12`. It affects only generated Plasma popup assets; inner controls retain one-pixel outlines. Reconfigure, rebuild, and reinstall after changing it:

```sh
cmake --preset dev -S . -DAZRAH_PLASMA_POPUP_BORDER_WIDTH=8
./scripts/dev install
```
