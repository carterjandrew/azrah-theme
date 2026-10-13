{
  description = "Azrah, a Breeze-derived theme for KDE Plasma";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

      mkAzrah = pkgs:
        pkgs.kdePackages.breeze.overrideAttrs (old: {
          pname = "azrah";
          version = "6.8.80";
          src = self;

          # Keep the legacy style in the dedicated qt5 output even though
          # non-Nix builds now default to Qt 6 only.
          cmakeFlags = (old.cmakeFlags or [ ]) ++ [ "-DBUILD_QT5=ON" ];

          postInstall = ''
            mkdir -p "$qt5/${pkgs.libsForQt5.qtbase.qtPluginPrefix}/styles"
            mv "$out/${pkgs.qt6.qtbase.qtPluginPrefix}/styles/azrah5.so" \
              "$qt5/${pkgs.libsForQt5.qtbase.qtPluginPrefix}/styles/"
          '';

          meta = (old.meta or { }) // {
            description = "Azrah widget style, window decoration, and theme suite for KDE Plasma";
            homepage = "https://github.com/carterjandrew/azrah-theme";
            mainProgram = "azrah-settings6";
          };
        });
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          azrah = mkAzrah pkgs;
        in
        {
          inherit azrah;
          default = azrah;
        }
      );

      checks = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          azrah = mkAzrah pkgs;
        in
        {
          package = azrah;
          coinstall-with-breeze = pkgs.buildEnv {
            name = "azrah-breeze-coinstall-check";
            paths = [
              pkgs.kdePackages.breeze
              (pkgs.lib.getOutput "qt5" pkgs.kdePackages.breeze)
              azrah
              (pkgs.lib.getOutput "qt5" azrah)
            ];
          };
        }
      );

      nixosModules.default =
        { config, lib, pkgs, ... }:
        let
          cfg = config.programs.azrah;
        in
        {
          options.programs.azrah = {
            enable = lib.mkEnableOption "the Azrah KDE Plasma theme suite";

            package = lib.mkOption {
              type = lib.types.package;
              default = mkAzrah pkgs;
              defaultText = lib.literalExpression "inputs.azrah.packages.${pkgs.stdenv.hostPlatform.system}.default";
              description = "The Azrah package to install.";
            };
          };

          config = lib.mkIf cfg.enable {
            environment.systemPackages = [
              cfg.package
              (lib.getOutput "qt5" cfg.package)
            ];
          };
        };
    };
}
