# Generated by Django 4.2.6 on 2024-01-10 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer_price', '0002_rename_worker_name_offerprice_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offerpricecomment',
            old_name='report',
            new_name='offer_price',
        ),
    ]