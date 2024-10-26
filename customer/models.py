import uuid
from django.db import models

from restaurent_manager.models import Product
from django.contrib.auth.models import User  

# Create your models here.
class Cart(models.Model):  
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')  
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='customer_id')  
    quantity = models.IntegerField()  


class Profile(models.Model):
     user_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
     contact=models.CharField(max_length=20)
     street=models.CharField(max_length=100)
     city=models.CharField(max_length=20)
     state=models.CharField(max_length=20)
     pincode=models.CharField(max_length=20)


class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')
    full_address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.pincode}"



class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)





class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    DELIVERY_STATUS_CHOICES = [
        ('Order Placed', 'Order Placed'),
        ('Processed', 'Processed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='Order Placed')
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pimage = models.ImageField(upload_to='image', null=True, blank=True)   # price at the time of order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='Order Placed')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)