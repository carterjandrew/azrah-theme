# Azrah

Azrah is a Breeze-derived theme suite for KDE Plasma. It installs alongside
Breeze with its own style, window-decoration, settings, color-scheme, cursor,
wallpaper, plugin, and translation identities.

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

## Components

- Qt widget styles: `Azrah` for Qt 6 and Qt 5
- KWin window decoration: `Azrah`
- Color schemes: `Azrah Classic`, `Azrah Dark`, and `Azrah Light`
- Cursor themes: `Azrah Dark` and `Azrah Light`
- Wallpaper: `Azrah (Hanabi)`
- Settings application: `azrah-settings6`

Azrah stores its settings in `azrahrc`, independently of Breeze's settings.

## Building without Nix

Azrah uses the standard KDE CMake build. Both Qt versions are enabled by
default; use `BUILD_QT5` and `BUILD_QT6` to control them. The current source
requires Qt 6.11, KDE Frameworks 6.30, and compatible Plasma development
libraries.

## Upstream and licensing

Azrah is based on KDE's
[Breeze](https://invent.kde.org/plasma/breeze) project. Original authorship and
license information is retained in the source tree and component metadata; see
`AUTHORS` and `LICENSES/`.
