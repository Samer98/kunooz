# Generated by Django 4.2.6 on 2024-01-08 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('additional_modification', '0006_rename_comment_additionalmodificationcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalmodification',
            name='note',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='additionalmodificationcomment',
            name='comment',
            field=models.TextField(),
        ),
    ]
