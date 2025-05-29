# Installation instructions for TibiaHouses

## Install with pip (from source)

1. Clone the repository:

   git clone https://github.com/{username}/TibiaHouses.git
   cd TibiaHouses

2. Install the package and dependencies:

   pip install .

## Development install

If you want to contribute or run tests:

   pip install -e .[dev]

## Build a distribution

   python -m build

## Run tests

   pytest

---

This project uses a modern pyproject.toml-based build. The old setup.py is no longer needed.
