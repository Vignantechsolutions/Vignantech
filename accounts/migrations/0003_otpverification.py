from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_testimonial_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField()),
                ('otp', models.CharField(max_length=6)),
                ('purpose', models.CharField(choices=[('register', 'Email Verification'), ('reset', 'Password Reset')], max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'OTP Verification',
                'verbose_name_plural': 'OTP Verifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
