#!/usr/bin/env python

"""
Using Faker

generate users fixture based on specified fields
"""

__author__ = "seyLu"
__github__ = "github.com/seyLu"

__licence__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "seyLu"
__status__ = "Prototype"

import logging
from logging.config import fileConfig
from pathlib import Path
from typing import Any

import phonenumbers
import yaml
from faker import Faker

Path("logs").mkdir(exist_ok=True)
fileConfig("logging.ini")

FIXTURES_PATH: str = "fixtures"
Path(FIXTURES_PATH).mkdir(exist_ok=True)
MODEL_NAME: str = "user"
YAML_FILENAME: str = f"{MODEL_NAME.capitalize()}.yaml"


def generate_fixture() -> None:
    _get_yaml()


def _get_yaml() -> None:
    logging.info(f"Generating {YAML_FILENAME}.")
    with open(f"{FIXTURES_PATH}/{YAML_FILENAME}", "w+") as f:
        print(
            yaml.dump(
                _get_fixtures(),
                default_flow_style=False,
                sort_keys=False,
            ),
            file=f,
        )


def _get_fixtures() -> list[dict[str, Any]]:
    logging.info(f"Serializing fixture {MODEL_NAME}.")

    fake = Faker(["en_PH"])
    Faker.seed(0)

    fixtures: list[dict[str, Any]] = []
    for pk in range(1, 21):
        is_email_verified: bool = fake.boolean(chance_of_getting_true=75)
        fixtures.append(
            {
                "model": f"users.{MODEL_NAME}",
                "pk": pk,
                "fields": {
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": fake.ascii_safe_email(),
                    "mobile_number": phonenumbers.format_number(
                        phonenumbers.parse(fake.mobile_number(), "PH"),
                        phonenumbers.PhoneNumberFormat.E164,
                    ),
                    "is_email_verified": is_email_verified,
                    "is_mobile_verified": fake.boolean(chance_of_getting_true=75),
                    "is_active": is_email_verified,
                    "is_staff": True if pk == 1 else False,
                },
            }
        )
    return fixtures


if __name__ == "__main__":
    generate_fixture()
