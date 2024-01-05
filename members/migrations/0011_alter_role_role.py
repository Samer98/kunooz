# Generated by Django 4.2.6 on 2024-01-02 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_remove_user_personal_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(blank=True, choices=[('Consultant', 'Consultant'), ('User', 'User'), ('Worker', 'Worker'), ('Owner', 'Owner')], max_length=255, null=True),
        ),
    ]