# Generated by Django 3.2.7 on 2021-10-31 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifiers', '0003_notifiers_title'),
        ('jobs', '0002_alter_jobs_notifiers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='notifiers',
            field=models.ManyToManyField(blank=True, db_column='uuid', related_name='jobs_notifiers', to='notifiers.Notifiers'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='title',
            field=models.CharField(max_length=15),
        ),
    ]
