# Generated by Django 4.2.6 on 2024-01-01 18:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('additional_modification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalmodification',
            name='date_created',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='additionalmodification',
            name='title',
            field=models.CharField(default='first', max_length=255),
            preserve_default=False,
        ),
    ]