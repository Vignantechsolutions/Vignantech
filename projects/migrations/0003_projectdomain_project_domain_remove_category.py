from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_algorithms_project_conclusion_and_more'),
    ]

    operations = [
        # 1. Create ProjectDomain table
        migrations.CreateModel(
            name='ProjectDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, help_text='e.g. AI & Machine Learning')),
                ('slug', models.SlugField(unique=True, help_text='e.g. aiml — used in URLs and CSS classes')),
                ('emoji', models.CharField(max_length=10, default='💻', help_text='Domain emoji shown on cards')),
                ('color_from', models.CharField(max_length=7, default='#1E3A8A', help_text='Gradient start hex color')),
                ('color_to', models.CharField(max_length=7, default='#3B82F6', help_text='Gradient end hex color')),
                ('badge_bg', models.CharField(max_length=30, default='rgba(59,130,246,.12)', help_text='Badge background (CSS rgba)')),
                ('badge_color', models.CharField(max_length=7, default='#1D4ED8', help_text='Badge text hex color')),
                ('description', models.TextField(blank=True, help_text='Short description shown on listing page')),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Project Domain',
                'verbose_name_plural': 'Project Domains',
                'ordering': ['order', 'name'],
            },
        ),
        # 2. Add nullable domain FK to Project
        migrations.AddField(
            model_name='project',
            name='domain',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='projects',
                to='projects.projectdomain',
                help_text='Select the project domain',
            ),
        ),
        # 3. Remove old category field
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
    ]
