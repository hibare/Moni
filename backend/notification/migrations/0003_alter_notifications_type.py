# Generated by Django 3.2.5 on 2021-07-19 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notifications_notificatio_uuid_d5968a_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='type',
            field=models.CharField(choices=[('slack', 'Slack'), ('discord', 'Discord')], max_length=10),
        ),
    ]