# TibiaHouses

[![Python application](https://github.com/Ojedalatronico/TibiaHouses/actions/workflows/python-app.yml/badge.svg)](https://github.com/Ojedalatronico/TibiaHouses/actions/workflows/python-app.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project scrapes and saves information about houses in Tibia.

## Features

- Scrapes house data from the official Tibia website
- Saves results as a CSV in the `data/` folder
- Modern Python project structure (`src/` and `tests/`)
- CLI support for easy usage and custom output path
- Fully tested with pytest

## Installation

```bash
pip install -e .
```

## Usage

### Command Line Interface (CLI)

Run the scraper and save results to the default location (`data/houses.csv`):

```bash
python -m tibiahouses.main
```

Or specify a custom output file:

```bash
python -m tibiahouses.main --output myhouses.csv
```

### As a Script

You can also use the provided script:

```bash
python scrape_houses.py
```

## Project Structure

```
├── data/                # Output CSV files
├── src/
│   └── tibiahouses/     # Main package code
├── tests/               # All tests
├── scrape_houses.py     # Example script entry point
├── setup.py             # Project metadata
├── requirements.txt     # Main dependencies
├── requirements-dev.txt # Dev/test dependencies
└── README.md
```

## Testing

Run all tests with:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
