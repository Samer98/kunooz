# Generated by Django 4.2.6 on 2023-12-29 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_user_projects_limits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='personal_date',
        ),
    ]
