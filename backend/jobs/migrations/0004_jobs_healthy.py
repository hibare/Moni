# Generated by Django 3.2.7 on 2021-11-06 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20211031_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='healthy',
            field=models.BooleanField(default=False),
        ),
    ]