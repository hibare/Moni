# Generated by Django 3.2 on 2021-06-03 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_alter_jobs_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='uuid',
            field=models.CharField(default='126a416f-aa58-41cf-b327-7d825095f4c2', max_length=40, primary_key=True, serialize=False),
        ),
    ]
