# Generated by Django 4.1.7 on 2024-05-25 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_rename_parallelization_file_parallelizations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='parallelizations',
            new_name='parallelization',
        ),
    ]