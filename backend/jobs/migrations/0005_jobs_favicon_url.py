# Generated by Django 3.2.7 on 2021-11-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_jobs_healthy'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='favicon_url',
            field=models.URLField(null=True),
        ),
    ]
