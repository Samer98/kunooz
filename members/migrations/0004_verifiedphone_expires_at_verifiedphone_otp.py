# Generated by Django 4.2.6 on 2023-12-17 11:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_verifiedphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifiedphone',
            name='expires_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verifiedphone',
            name='otp',
            field=models.CharField(default=1111, max_length=6),
            preserve_default=False,
        ),
    ]
