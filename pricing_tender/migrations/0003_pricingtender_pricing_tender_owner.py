# Generated by Django 4.2.6 on 2024-01-18 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pricing_tender', '0002_rename_contractor_pricingtendercontractor_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricingtender',
            name='pricing_tender_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
