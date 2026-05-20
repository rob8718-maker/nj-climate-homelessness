"""
make_dataset.py
---------------
Entry point for the data pipeline.
Reads raw data, applies cleaning, writes processed outputs.

Usage:
    python -m src.data.make_dataset
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def main():
    log.info("Starting data pipeline...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    # TODO: call individual loaders for HUD PIT, NOAA, NASA SEDAC
    log.info("Pipeline complete.")


if __name__ == "__main__":
    main()
