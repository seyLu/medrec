#!/usr/bin/env python

"""
Generate fixtures in order.
"""

__author__ = "seyLu"
__github__ = "github.com/seyLu"

__licence__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "seyLu"
__status__ = "Prototype"

import logging
import subprocess
from logging.config import fileConfig
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
fileConfig("logging.ini")

apps: list[str] = [
    "regions",
    "users",
    "clients",
    "records",
]

if __name__ == "__main__":
    for app in apps:
        logging.info(f"Generating fixture for app {app}.")
        subprocess.call(
            [
                "python",
                f"scripts/generate_{app}_fixture.py",
            ]
        )
