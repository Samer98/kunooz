# Generated by Django 4.2.6 on 2023-12-29 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constructions', '0006_rename_member_projectmember_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectmember',
            old_name='phone_number',
            new_name='member',
        ),
    ]