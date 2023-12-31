#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py tailwind install
python manage.py tailwind build

python manage.py collectstatic --no-input
python manage.py migrate

python scripts/loaddata_all.py
