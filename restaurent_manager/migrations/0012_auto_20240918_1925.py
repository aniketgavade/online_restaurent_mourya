# Generated by Django 3.0.5 on 2024-09-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurent_manager', '0011_remove_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Deliverable',
            field=models.BooleanField(default=False),
        ),
    ]
