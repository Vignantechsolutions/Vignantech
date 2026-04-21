#!/usr/bin/env bash
set -o errexit
python manage.py loaddata all_data.json
echo "Data loaded successfully!"
