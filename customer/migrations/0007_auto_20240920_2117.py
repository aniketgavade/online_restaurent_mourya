# Generated by Django 3.0.5 on 2024-09-20 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20240920_2116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='product_id',
            new_name='product',
        ),
    ]
