# Developing Azrah

## Supported development target

The primary target is Plasma 6 on Linux with Qt 6. The default preset builds the Azrah Qt widget style, settings tools, KWin decoration, and existing tests.

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

Set `AZRAH_INSTALL_PREFIX` before `configure` to use a prefix other than `~/.local`. For a custom prefix, add its `lib/qt6/plugins` directory to `QT_PLUGIN_PATH` before launching test applications.

The first default-prefix install creates `~/.config/environment.d/azrah.conf`. A full logout/login is required for Plasma to inherit it. Uninstall removes that file and CMake-installed files, but deliberately leaves directories and user settings intact.

## Testing changes

After installing, use a small Qt/KDE application to check common controls before changing the whole desktop. Force the style for one process with:

```sh
QT_STYLE_OVERRIDE=Azrah systemsettings
```

Check light and dark system schemes. For widgets, cover normal, hovered, focused, pressed, checked, disabled, and destructive states. For decorations, check active/inactive, maximized and tiled windows, every border size, and high-DPI scaling.

Development scripts do not restart or replace KWin. After installing a decoration change, reselect Azrah or log out and back in. Keep Breeze available as the recovery style.

## Troubleshooting

- If configuration reports ECM missing, install `extra-cmake-modules` (it is missing on the original development machine at the time of writing).
- If Azrah is absent from Application Style, confirm `~/.local/lib/qt6/plugins` is in `QT_PLUGIN_PATH` and start a new login session.
- If metadata looks stale, run `kbuildsycoca6`.
- If an application does not refresh after saving, restart it while investigating the Azrah D-Bus reload signal.
- If the desktop becomes difficult to use, choose Breeze again. `./scripts/dev uninstall` does not touch Breeze.

## Incorporating upstream Breeze

```sh
git remote add upstream https://invent.kde.org/plasma/breeze.git
git fetch upstream
```

This checkout may be shallow; use `git fetch --unshallow origin` if history is required before a rebase. Rebase or merge upstream in a dedicated branch, keep the public Azrah identity changes, and avoid broad internal `Breeze::` or filename renames. Then run the full workflow and inspect a staged install for accidental `org.kde.breeze`, `breezerc`, or Breeze plugin filenames.

## Build options

Direct CMake users may control `BUILD_QT5`, `BUILD_QT6`, `BUILD_STYLE`, `BUILD_COLORS`, `BUILD_CURSOR`, `BUILD_MISC`, `BUILD_WITH_QTQUICK`, `WITH_DECORATIONS`, and `WITH_WALLPAPERS`.
