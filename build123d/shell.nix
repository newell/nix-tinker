# shell.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable";
  pkgs = import nixpkgs { config = {}; overlays = []; };

  # pkgs = import <nixpkgs> {};

  python = pkgs.python3.override {
    self = python;
    packageOverrides = pyfinal: pyprev: {
        build123d = pyfinal.callPackage ./build123d.nix { };
    };
  };
in (pkgs.buildFHSEnv {
  name = "build123d";
  targetPkgs = pkgs: (with pkgs; [
    (python.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.build123d
    ]))
  ]);
}).env
