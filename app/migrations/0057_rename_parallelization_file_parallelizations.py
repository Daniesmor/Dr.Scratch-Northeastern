# Generated by Django 4.1.7 on 2024-05-25 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_alter_file_options_alter_file_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='parallelization',
            new_name='parallelizations',
        ),
    ]