# Generated by Django 3.2.9 on 2021-12-05 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifiers", "0005_auto_20211205_0754"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notifiers",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
    ]
