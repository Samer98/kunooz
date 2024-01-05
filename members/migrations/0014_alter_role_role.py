# Generated by Django 4.2.6 on 2024-01-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_alter_role_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(blank=True, choices=[('Consultant', 'Consultant'), ('User', 'User'), ('Worker', 'Worker')], max_length=255, null=True),
        ),
    ]