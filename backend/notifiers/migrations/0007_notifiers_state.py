# Generated by Django 4.2.1 on 2023-06-08 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifiers', '0006_alter_notifiers_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifiers',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]