# Generated by Django 3.2 on 2021-05-16 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20210516_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobs',
            old_name='description',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='jobs',
            name='uuid',
            field=models.CharField(default='726bb173-a9b7-48e7-95b3-3c39ebccde58', max_length=40, primary_key=True, serialize=False),
        ),
    ]
