{ lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  
  # dependencies
  addict,
  appdirs,
  colour,
  diskcache,
  ipython,
  isosurfaces,
  fonttools,
  manimpango,
  mapbox-earcut,
  matplotlib,
  moderngl,
  moderngl-window,
  numpy,
  pillow,
  pydub,
  pygments,
  pyopengl,
  pyperclip,
  pyyaml,
  rich,
  scipy,
  screeninfo,
  skia-pathops,
  svgelements,
  sympy,
  tqdm,
  typing-extensions,
  validators,
}:

buildPythonPackage rec {
  pname = "manimgl";
  version = "1.7.2";
  pyproject = true;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-WkZy/zg0khhxx5oINGLepwalfLWi6IA6SPVTPQ9tGVY=";
  };

  dependencies = [
    addict
    appdirs
    colour
    diskcache
    ipython
    isosurfaces
    fonttools
    manimpango
    mapbox-earcut
    matplotlib
    moderngl
    moderngl-window
    numpy
    pillow
    pydub
    pygments
    pyopengl
    pyperclip
    pyyaml
    rich
    scipy
    screeninfo
    skia-pathops
    svgelements
    sympy
    tqdm
    typing-extensions
    validators
  ];

  build-system = [
    setuptools wheel
  ];

  # has no tests
  doCheck = false;

#  pythonImportsCheck = [
#    "manimlib"
#  ];

  meta = {
    description = "Animation engine for explanatory math videos";
    longDescription = ''
      Manim is an animation engine for explanatory math videos. It's used to
      create precise animations programmatically, as seen in the videos of
      3Blue1Brown on YouTube.
    '';
    homepage = "https://github.com/3b1b/manim";
    license = lib.licenses.mit;
    maintainers = [ ];
  };
}