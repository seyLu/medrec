#!/usr/bin/env python

"""
Loaddata helper.
"""

__author__ = "seyLu"
__github__ = "github.com/seyLu"

__licence__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "seyLu"
__status__ = "Prototype"

import logging
import os
import subprocess
from logging.config import fileConfig
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
fileConfig("logging.ini")

LOADDATA_COMMAND: list[str] = [
    "python",
    "manage.py",
    "loaddata",
]
FIXTURE_PATH: str = "fixtures"


def loaddata(fixtures: list[str], ext: str = "yaml") -> None:
    """
    Loads all fixtures in order.
    """

    for fixture in fixtures:
        fixture = f"{fixture}.{ext}"
        logging.info(f"Loading fixture {fixture}.")

        subprocess.call([*LOADDATA_COMMAND, os.path.join(FIXTURE_PATH, fixture)])
