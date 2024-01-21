# Generated by Django 4.2.6 on 2024-01-18 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pricing_tender', '0005_rename_pricingtender_offerprice_pricing_tender'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerprice',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
