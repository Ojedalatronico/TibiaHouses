#!/usr/bin/env python3
"""Script to run the Tibia houses scraper."""

import asyncio
from tibiahouses.main import main  # type: ignore

if __name__ == "__main__":
    asyncio.run(main())
