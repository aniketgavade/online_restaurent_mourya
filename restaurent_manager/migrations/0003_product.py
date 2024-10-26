# Generated by Django 3.0.5 on 2024-08-31 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurent_manager', '0002_auto_20240827_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('is_active', models.BooleanField()),
                ('image', models.ImageField(upload_to='image')),
                ('category_id', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.CASCADE, to='restaurent_manager.Category')),
                ('seller_id', models.ForeignKey(db_column='seller_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
