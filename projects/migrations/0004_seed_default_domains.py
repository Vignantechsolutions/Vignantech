from django.db import migrations


DEFAULT_DOMAINS = [
    {
        'name': 'AI & Machine Learning',
        'slug': 'aiml',
        'emoji': '🤖',
        'color_from': '#1E3A8A',
        'color_to': '#3B82F6',
        'badge_bg': 'rgba(59,130,246,.12)',
        'badge_color': '#1D4ED8',
        'description': 'Intelligent systems, deep learning, computer vision, NLP and predictive models.',
        'order': 1,
    },
    {
        'name': 'Python Full Stack',
        'slug': 'python',
        'emoji': '🐍',
        'color_from': '#065F46',
        'color_to': '#10B981',
        'badge_bg': 'rgba(16,185,129,.12)',
        'badge_color': '#065F46',
        'description': 'Django / Flask web applications with MySQL, REST APIs and Bootstrap frontends.',
        'order': 2,
    },
    {
        'name': 'MERN Stack',
        'slug': 'mern',
        'emoji': '🌐',
        'color_from': '#1E1B4B',
        'color_to': '#7C3AED',
        'badge_bg': 'rgba(124,58,237,.12)',
        'badge_color': '#6D28D9',
        'description': 'MongoDB, Express, React and Node.js full-stack web applications.',
        'order': 3,
    },
    {
        'name': 'Java Full Stack',
        'slug': 'java',
        'emoji': '☕',
        'color_from': '#78350F',
        'color_to': '#F59E0B',
        'badge_bg': 'rgba(245,158,11,.12)',
        'badge_color': '#92400E',
        'description': 'Spring Boot, Hibernate, JSP/Servlet and Java-based enterprise applications.',
        'order': 4,
    },
    {
        'name': 'Data Science',
        'slug': 'datascience',
        'emoji': '📊',
        'color_from': '#831843',
        'color_to': '#EC4899',
        'badge_bg': 'rgba(236,72,153,.12)',
        'badge_color': '#9D174D',
        'description': 'Data analysis, visualization, statistical modelling and business intelligence.',
        'order': 5,
    },
]


def seed_domains(apps, schema_editor):
    ProjectDomain = apps.get_model('projects', 'ProjectDomain')
    for d in DEFAULT_DOMAINS:
        ProjectDomain.objects.get_or_create(slug=d['slug'], defaults=d)


def unseed_domains(apps, schema_editor):
    pass  # keep data on reverse


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_projectdomain_project_domain_remove_category'),
    ]

    operations = [
        migrations.RunPython(seed_domains, unseed_domains),
    ]
