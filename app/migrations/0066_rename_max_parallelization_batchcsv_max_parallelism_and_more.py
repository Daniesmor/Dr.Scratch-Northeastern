# Generated by Django 4.1.7 on 2025-02-08 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0065_rename_metrics_file_extended_metrics'),
    ]

    operations = [
        migrations.RenameField(
            model_name='batchcsv',
            old_name='max_parallelization',
            new_name='max_parallelism',
        ),
        migrations.RenameField(
            model_name='batchcsv',
            old_name='parallelization',
            new_name='parallelism',
        ),
    ]
