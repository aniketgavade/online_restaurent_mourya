# Generated by Django 3.0.5 on 2024-09-18 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurent_manager', '0006_auto_20240901_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='status',
            new_name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]
