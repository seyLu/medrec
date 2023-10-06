#!/usr/bin/env python

"""
Using Faker

generate clients fixture based on specified fields
"""

__author__ = "seyLu"
__github__ = "github.com/seyLu"

__licence__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "seyLu"
__status__ = "Prototype"

import logging
import random
import re
from copy import deepcopy
from datetime import datetime
from logging.config import fileConfig
from pathlib import Path
from typing import Any

import yaml
from faker import Faker
from gpt4all import GPT4All

Path("logs").mkdir(exist_ok=True)
fileConfig("logging.ini")

FIXTURES_PATH: str = "fixtures"
Path(FIXTURES_PATH).mkdir(exist_ok=True)
MODEL_NAME: str = "record"
YAML_FILENAME: str = f"{MODEL_NAME.capitalize()}.yaml"

Path(".venv/gpt4all/").mkdir(exist_ok=True)
model: GPT4All = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin", ".venv/gpt4all/")

history_message: str = """
    Give an example medical history that a human might present to a doctor.
    Just give me the medical history and nothing else.
"""
diagnosis_and_plan_message: str = (
    "From the medical history you provided, provide a medical diagnosis and plan."
)


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


def _load_yaml(yaml_path: str) -> list[dict[str, Any]]:
    with open(yaml_path) as f:
        return [item["fields"] for item in yaml.safe_load(f)]


CLIENTS: list[dict[str, Any]] = _load_yaml("fixtures/Client.yaml")


def get_client() -> Any:
    return random.choice(CLIENTS[:1])


sample_client = get_client()


def _get_fixtures() -> list[dict[str, Any]]:
    logging.info(f"Serializing fixture {MODEL_NAME}.")

    fake = Faker(["en_PH"])
    Faker.seed(0)

    fixtures: list[dict[str, Any]] = []
    for pk in range(1, 2):
        created_datetime: datetime = fake.date_time()
        updated_datetime: datetime = fake.date_time_between_dates(created_datetime)
        client: str = sample_client["reference_number"]
        with model.chat_session():
            history: str = model.generate(
                history_message
                + f"\nUse client name {sample_client['first_name']} {sample_client['last_name']} and age {sample_client['age']} as an example."
            )
            diagnosis_and_plan: str = model.generate(diagnosis_and_plan_message)
        history = re.sub(
            r"(?:\s|\\)*Sure, here[']*s an example of a medical history that a human might present(?:\s|\\)*to a doctor:(?:\s|\\|\n)*(?:---)?(?:\n)*",
            "",
            history,
        )

        remarks: str = ""
        is_seen_by_staff: bool = fake.boolean(chance_of_getting_true=25)

        fixtures.append(
            {
                "model": f"records.{MODEL_NAME}",
                "pk": pk,
                "fields": {
                    "created_datetime": created_datetime,
                    "updated_datetime": updated_datetime,
                    "client": client,
                    "history": history,
                    "diagnosis_and_plan": diagnosis_and_plan,
                    "remarks": remarks,
                    "is_seen_by_staff": is_seen_by_staff,
                },
            }
        )

    for pk in range(2, 6):
        fixtures_copy = deepcopy(fixtures[0])
        fixtures_copy["pk"] = pk
        fixtures_copy["created_datetime"] = fake.date_time()
        fixtures_copy["updated_datetime"] = fake.date_time_between_dates(
            fixtures_copy["created_datetime"]
        )
        fixtures.append(fixtures_copy)

    return fixtures


if __name__ == "__main__":
    generate_fixture()
