# Azrah

Azrah is a sharp, restrained KDE theme suite derived from Breeze. It installs
alongside Breeze with its own application style, KWin decoration, Plasma theme,
settings, color schemes, cursors, wallpaper, plugin, and translation identities.
It keeps Breeze's integration with KDE system colors while moving toward square
geometry, clear borders, and simple two-tone interaction states.

## NixOS

### Flake-based configuration

Add Azrah to your NixOS flake inputs, import its module, and enable it. Replace
`my-machine` with your existing NixOS configuration name:

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    azrah = {
      url = "github:carterjandrew/azrah-theme";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, azrah, ... }: {
    nixosConfigurations.my-machine = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        azrah.nixosModules.default
        ({ ... }: {
          programs.azrah.enable = true;
        })
      ];
    };
  };
}
```

Keep `inputs.azrah.inputs.nixpkgs.follows = "nixpkgs"` in place. Azrah is
derived from `pkgs.kdePackages.breeze`, so following the system's nixpkgs input
keeps its Qt, KDE Frameworks, and Plasma libraries aligned with the rest of the
system instead of introducing a second KDE package set.

Then rebuild your system from the directory containing your `flake.nix`:

```sh
sudo nixos-rebuild switch --flake .#my-machine
```

The module installs the complete Azrah theme suite, including both the Qt 6 and
Qt 5 widget styles. It deliberately does not change an existing user's active
theme. After rebuilding, open **System Settings → Colors & Themes** and select
Azrah for the components you want to use:

- **Application Style:** Azrah
- **Window Decorations:** Azrah
- **Colors:** Azrah Classic, Azrah Dark, or Azrah Light
- **Cursors:** Azrah Dark or Azrah Light
- **Wallpaper:** Azrah (Hanabi)

To update Azrah later, update the input and rebuild:

```sh
nix flake update azrah
sudo nixos-rebuild switch --flake .#my-machine
```

### Package-only installation

If you do not want to use the supplied NixOS module, add the package outputs to
`environment.systemPackages` yourself:

```nix
{ inputs, lib, pkgs, ... }:

let
  azrah = inputs.azrah.packages.${pkgs.stdenv.hostPlatform.system}.default;
in
{
  environment.systemPackages = [
    azrah
    (lib.getOutput "qt5" azrah)
  ];
}
```

Using the module is recommended because it installs the Qt 5 output correctly
without relying on the package output attribute layout.

The package can also be built directly:

```sh
nix build github:carterjandrew/azrah-theme
```
The project is early in development. The current milestone establishes a collision-free identity and a repeatable development workflow; the visual work comes next.

- Qt widget styles: `Azrah` for Qt 6 and Qt 5
- KWin window decoration: `Azrah`
- Color schemes: `Azrah Classic`, `Azrah Dark`, and `Azrah Light`
- Cursor themes: `Azrah Dark` and `Azrah Light`
- Wallpaper: `Azrah (Hanabi)`
- Settings application: `azrah-settings6`

Azrah stores its settings in `azrahrc`, independently of Breeze's settings.

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

## Building without Nix

Azrah uses the standard KDE CMake build. Manual builds enable Qt 6 by default;
pass `-DBUILD_QT5=ON` to include the legacy Qt 5 style. The Nix package enables
both versions and places the Qt 5 plugin in its separate `qt5` output. The
current source requires Qt 6.11, KDE Frameworks 6.26, and compatible Plasma
development libraries.

## Relationship to Breeze

Azrah preserves many internal Breeze filenames, targets, and C++ namespaces. This is deliberate: public and installed identifiers use Azrah, while internal continuity makes it easier to review changes and incorporate useful fixes from upstream.

KDE Breeze is developed at <https://invent.kde.org/plasma/breeze>. Original copyrights and SPDX license declarations are retained. Azrah remains distributed under the licenses declared by each source file and in `LICENSES/`.
