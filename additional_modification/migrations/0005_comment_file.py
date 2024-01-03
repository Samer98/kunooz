# Generated by Django 4.2.6 on 2024-01-03 15:48

import additional_modification.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('additional_modification', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='additional_modification_comment_files', validators=[additional_modification.models.validate_file_size]),
        ),
    ]
