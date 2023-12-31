# Generated by Django 4.2.6 on 2024-01-01 18:38

import additional_modification.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('constructions', '0007_rename_phone_number_projectmember_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='additional_modification_files', validators=[additional_modification.models.validate_file_size])),
                ('note', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constructions.project')),
            ],
        ),
    ]
