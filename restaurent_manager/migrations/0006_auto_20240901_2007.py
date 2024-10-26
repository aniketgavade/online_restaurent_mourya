# Generated by Django 3.0.5 on 2024-09-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurent_manager', '0005_auto_20240831_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='food_description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
