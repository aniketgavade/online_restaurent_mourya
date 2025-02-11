# Generated by Django 3.0.5 on 2024-09-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0024_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processed', 'Processed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Successful', max_length=50),
        ),
    ]
