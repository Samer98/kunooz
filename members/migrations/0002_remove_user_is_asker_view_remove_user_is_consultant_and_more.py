# Generated by Django 4.2.6 on 2023-12-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_asker_view',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_consultant',
        ),
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(blank=True, choices=[('Consultant', 'Consultant'), ('User', 'User'), ('Worker', 'Worker')], max_length=255, null=True),
        ),
    ]
