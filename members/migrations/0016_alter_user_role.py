# Generated by Django 4.2.6 on 2024-01-05 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_alter_role_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='members.role'),
        ),
    ]