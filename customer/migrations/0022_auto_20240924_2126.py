# Generated by Django 3.0.5 on 2024-09-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0021_auto_20240924_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='pimage',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
