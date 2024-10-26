from django.db import models
from django.contrib.auth.models   import User



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)


class Product(models.Model):
    restaurent_manager_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='restaurent_manager_id')
    food_name = models.CharField(max_length=25)
    food_price = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')
    food_description = models.CharField(max_length=1000)

    image = models.ImageField(upload_to='image')

    Deliverable = models.BooleanField(default=False)  # Default to 'False'

