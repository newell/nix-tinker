# shell.nix
let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable";
  pkgs = import nixpkgs { config = {}; overlays = []; };

  # pkgs = import <nixpkgs> {};

  python = pkgs.python3.override {
    self = python;
    packageOverrides = pyfinal: pyprev: {
        manimgl = pyfinal.callPackage ./manimgl.nix { };
    };
  };
in (pkgs.buildFHSEnv {
  name = "manimgl";
  targetPkgs = pkgs: (with pkgs; [
    (python.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.manimgl
    ]))
  ] ++ [libGL]);
}).env
#in pkgs.mkShell {
#  packages = [
#    (python.withPackages (python-pkgs: [
#      # select Python packages here
#      python-pkgs.manimce
#    ]))
#  ];
#}
