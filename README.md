# Azrah

Azrah is a sharp, restrained KDE application style, KWin decoration, and companion Plasma theme derived from KDE's Breeze. It keeps Breeze's integration with KDE system colors while moving toward square geometry, clear borders, and simple two-tone interaction states.

The project is early in development. The current milestone establishes a collision-free identity and a repeatable development workflow; the visual work comes next.

## Quick start

```sh
./scripts/dev doctor
./scripts/dev configure
./scripts/dev build
./scripts/dev test
./scripts/dev install
```

The development preset builds the Qt 6 widget style and KWin decoration. It intentionally excludes the inherited Breeze colors, cursors, wallpapers, Qt 5 style, and miscellaneous utilities.

The install command uses `~/.local`, refreshes KDE's service cache, and configures the user Qt plugin path. Log out and back in after the first install, then select **Azrah** under **System Settings → Colors & Themes → Application Style**, **Window Decorations**, and **Plasma Style**.

To remove only the files recorded by the development install:

```sh
./scripts/dev uninstall
```

See [Development](docs/development.md) for dependencies, troubleshooting, and the upstream workflow. See [Design direction](docs/design.md) for visual principles and the [development log](docs/devlog.md) for notable implementation findings.

## Relationship to Breeze

Azrah preserves many internal Breeze filenames, targets, and C++ namespaces. This is deliberate: public and installed identifiers use Azrah, while internal continuity makes it easier to review changes and incorporate useful fixes from upstream.

KDE Breeze is developed at <https://invent.kde.org/plasma/breeze>. Original copyrights and SPDX license declarations are retained. Azrah remains distributed under the licenses declared by each source file and in `LICENSES/`.
