# Generated by Django 5.1.1 on 2024-09-28 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurent_manager', '0013_remove_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
