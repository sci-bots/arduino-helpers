Conda recipe to build `arduino-helpers` package.

Build
=====

Install `conda-build`:

    conda install conda-build

Build recipe:

    conda build . -m variants.yaml


Install
=======

The pre-built package may be installed from the [`sci-bots`][2] channel using:

    conda install -c sci-bots arduino-helpers


[1]: https://anaconda.org/sci-bots/clang
[2]: https://anaconda.org/sci-bots
