import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vignan_tech.settings')
django.setup()
from projects.models import Project
print("Total:", Project.objects.count())
for p in Project.objects.all():
    print(p.id, p.category, p.title)
