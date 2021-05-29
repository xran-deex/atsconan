# ats-conan

This package is a simple subclass of ConanFile that sets some defaults for building ATS packages, specifically the -IATS include paths for all the package's dependencies

## Installation
```bash
pip install ./dist/atsconan-0.1.0.tar.gz
```

## Build
To build the package from source, install poetry (https://python-poetry.org)

```bash
python -m venv .venv
poetry shell
poetry install
poetry build
```
