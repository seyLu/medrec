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
from datetime import datetime
from logging.config import fileConfig
from pathlib import Path
from typing import Any

import yaml
from faker import Faker

Path("logs").mkdir(exist_ok=True)
fileConfig("logging.ini")

FIXTURES_PATH: str = "fixtures"
Path(FIXTURES_PATH).mkdir(exist_ok=True)
MODEL_NAME: str = "client"
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


def get_client_type() -> str:
    return random.choice(["TCH", "NTP", "STU"])


def get_rand_with_n_digits(d: int) -> int:
    return random.randrange(10 ** (d - 1), 10**d)


def get_reference_number(client_type: str) -> int:
    reference_number: int = -1
    if client_type == "STU":
        reference_number = get_rand_with_n_digits(12)
    else:
        reference_number = get_rand_with_n_digits(6)
    return reference_number


def get_age(client_type: str) -> int:
    if client_type == "STU":
        return random.randrange(4, 18)
    else:
        return random.randrange(18, 70)


def get_level(client_type: str, age: int) -> str:
    def get_student_level(age: int) -> str:
        if age < 6:
            return "Preschooler"
        if age == 18:
            return "Grade 12"
        if age > 18:
            raise ValueError("College level not supported")

        return f"Grade {age - 5}"

    def get_teacher_level(age: int) -> str:
        if age > 40:
            return "Senior Teacher"
        if age < 22:
            return "Student Teacher"
        if age < 30:
            return random.choice(
                [f"Teacher {random.randrange(1,2)}", "Assistant Teacher"]
            )

        return f"Teacher {random.randrange(3,4)}"

    def get_non_teaching_personnel_level(age: int) -> str:
        if age > 40:
            return random.choice(["Principal", "Vice Principal"])

        return random.choice(
            [
                "Secretary",
                "Guard",
                "Accountant",
                "Utility Personnel",
            ]
        )

    client_level_map: dict[str, str] = {
        "STU": get_student_level(age),
        "TCH": get_teacher_level(age),
        "NTP": get_non_teaching_personnel_level(age),
    }
    return client_level_map[client_type]


def get_building_name(building_name: str) -> str:
    building_name = re.sub(
        r"Building(s)?|Condominium(s)?|Tower(s)?|Place(s)?|Apartment(s)?|Residence(s)?|Suite(s)",
        "",
        building_name,
    )
    return " ".join(building_name.split())


def get_school(client_type: str, age: int) -> str:
    if client_type == "STU":
        if age < 6:
            return "Preschool"
        if age in range(6, 13):
            return "Elementary School"
        elif age in range(13, 17):
            return "High School"
        else:
            return "Senior High School"
    else:
        return random.choice(
            ["Preschool", "Elementary School", "High School", "Senior High School"]
        )


def _load_yaml(yaml_path: str) -> list[dict[str, Any]]:
    with open(yaml_path) as f:
        return [item["fields"] for item in yaml.safe_load(f)]


PROVINCES: list[dict[str, Any]] = _load_yaml("fixtures/Province.yaml")
CITIES: list[dict[str, Any]] = _load_yaml("fixtures/City.yaml")
DISTRICTS: list[dict[str, Any]] = _load_yaml("fixtures/District.yaml")


def get_province(region: str) -> Any:
    filtered_provinces = [
        province for province in PROVINCES if province["region"] == region
    ]
    return random.choice(filtered_provinces)["code"]


def get_city(province: str) -> Any:
    filtered_cities = [city for city in CITIES if city["province"] == province]
    return random.choice(filtered_cities)["code"]


def get_district(city: str) -> Any:
    filtered_districts = [
        district for district in DISTRICTS if district["city"] == city
    ]
    return random.choice(filtered_districts)["code"]


def _get_fixtures() -> list[dict[str, Any]]:
    logging.info(f"Serializing fixture {MODEL_NAME}.")

    fake = Faker(["en_PH"])
    Faker.seed(0)

    fixtures: list[dict[str, Any]] = []
    for pk in range(1, 101):
        client_type: str = get_client_type()
        age: int = get_age(client_type)
        level: str = get_level(client_type, age)
        region: str = "080000000"
        province: str = get_province(region)
        city: str = get_city(province)
        district: str = get_district(city)
        created_datetime: datetime = fake.date_time()
        updated_datetime: datetime = fake.date_time_between_dates(created_datetime)
        school: str = (
            f"{get_building_name(fake.building_name())} {get_school(client_type, age)}"
        )

        fixtures.append(
            {
                "model": f"clients.{MODEL_NAME}",
                "pk": pk,
                "fields": {
                    "reference_number": get_reference_number(client_type),
                    "type": client_type,
                    "age": age,
                    "level": level,
                    "created_datetime": created_datetime,
                    "updated_datetime": updated_datetime,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "school": school,
                    "region": region,
                    "province": province,
                    "city": city,
                    "district": district,
                    "street_address": fake.street_address(),
                },
            }
        )
    return fixtures


if __name__ == "__main__":
    generate_fixture()
