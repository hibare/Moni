# Generated by Django 3.2.5 on 2021-07-28 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_alter_notifications_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='type',
            field=models.CharField(choices=[('slack', 'Slack'), ('discord', 'Discord'), ('webhook', 'Webhook'), ('gotify', 'Gotify')], max_length=10),
        ),
    ]