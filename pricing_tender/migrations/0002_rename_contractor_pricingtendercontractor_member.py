# Generated by Django 4.2.6 on 2024-01-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing_tender', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricingtendercontractor',
            old_name='contractor',
            new_name='member',
        ),
    ]