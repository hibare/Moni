# Generated by Django 3.2.5 on 2021-07-18 18:21

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import jobs.models
import moni.utils.funcs


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('uuid', models.CharField(default=moni.utils.funcs.get_str_uuid, max_length=40, primary_key=True, serialize=False)),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=50)),
                ('state', models.BooleanField(default=True)),
                ('headers', models.JSONField(default=dict)),
                ('verify_ssl', models.BooleanField(default=True)),
                ('interval', models.IntegerField(default=15)),
                ('success_status', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=jobs.models.default_success_status, size=None)),
                ('check_redirect', models.BooleanField(default=True)),
                ('notification_urls', models.ManyToManyField(db_column='uuid', null=True, related_name='jobs_notification', to='notification.Notifications')),
            ],
            options={
                'verbose_name': 'Jobs',
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='JobsHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status_code', models.IntegerField(null=True)),
                ('success', models.BooleanField()),
                ('response_time', models.FloatField(null=True)),
                ('uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs_history_uuid', to='jobs.jobs')),
            ],
            options={
                'verbose_name': 'Jobs History',
                'verbose_name_plural': 'Jobs History',
            },
        ),
    ]
