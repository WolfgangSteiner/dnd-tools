{
  description = "DND paper templates with python";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = [
        pkgs.python310
        pkgs.python310Packages.numpy
        pkgs.python310Packages.svglib
        pkgs.python310Packages.typer
        pkgs.python310Packages.pillow
        pkgs.python310Packages.reportlab
        pkgs.python310Packages.pyyaml
      ];
    };
  };
}
