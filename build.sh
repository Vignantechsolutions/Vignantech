#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin@vignantechsolutions.com').exists():
    User.objects.create_superuser(username='admin@vignantechsolutions.com', email='admin@vignantechsolutions.com', password='Vignan@2024')
    print('Admin created')
else:
    print('Admin already exists')
"
