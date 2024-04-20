from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# App users
class Users(AbstractUser):
    user_id=models.CharField(max_length=10,primary_key=True)
    username = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True,max_length=150)
    password = models.CharField(max_length=300)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number=models.CharField(max_length=10)
    user_type=models.CharField(max_length=10,choices=[('Admin', 'Admin'),('User', 'User'),('Retailer', 'Retailer')])
    created_at=models.DateTimeField(auto_now_add=True)
    is_golden=models.BooleanField(default=False)
    
# Specifications for Products
class Specifications(models.Model):
    spec_id=models.CharField(max_length=10,primary_key=True)
    color=models.CharField(max_length=20)
    dimensions=models.CharField(max_length=20)
    size=models.CharField(max_length=20)
    material=models.CharField(max_length=20)
    weight=models.CharField(max_length=20)
    manufacturer=models.CharField(max_length=20)

# Product Categories
class Categories(models.Model):
    category_id=models.CharField(primary_key=True,max_length=10)
    category_name=models.CharField(max_length=20)
    
# User Addresses
class Addresses(models.Model):
    address_id = models.CharField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(Users,default=None,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number=models.CharField(max_length=10)
    address = models.TextField()
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    landmark = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    
# User Cards saved for quick payment
class Cards(models.Model):
    card_id = models.CharField(max_length=15, primary_key=True)
    user_id = models.ForeignKey(Users,default=None,on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    pin = models.IntegerField()
    card_type = models.CharField(max_length=6, choices=[('Debit','Debit'),('Credit','Credit')])
    expiry_date = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    
# App Products
class Products(models.Model):
    product_id = models.CharField(max_length=15,primary_key=True)
    product_name = models.CharField(max_length=100)
    spec_id = models.ForeignKey(Specifications, default=None, on_delete=models.CASCADE)
    description = models.TextField()
    category_id = models.ForeignKey(Categories, default=None, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    
# User Cart
class Carts(models.Model):
    cart_id = models.CharField(max_length=15,primary_key=True)
    product_id = models.ForeignKey(Products, default=None, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    
# User's Wishlists 
class Wishlists(models.Model):
    wishlist_id = models.CharField(max_length=15,primary_key=True)
    product_id = models.ForeignKey(Products, default=None, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, default=None, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    
# Product reviews made by users
class Reviews(models.Model):
    review_id = models.CharField(max_length=15, primary_key=True)
    product_id = models.ForeignKey(Products, default=None, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, default=None, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    
# Images for all the products
class ProductImages(models.Model):
    product_image_id = models.CharField(max_length=15, primary_key=True)
    product_id = models.ForeignKey(Products, default=None, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50, default=None)

# Images for all reviews 
class ReviewImages(models.Model):
    review_image_id = models.CharField(max_length=15, primary_key=True)
    review_id = models.ForeignKey(Reviews, default=None, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50, default=None)
    
# All orders made by users
class Orders(models.Model):
    order_id = models.CharField(max_length=15, primary_key=True)
    user_id = models.ForeignKey(Users, default=None, on_delete=models.CASCADE)
    total = models.FloatField()
    discounts = models.IntegerField()
    grand_total = models.FloatField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'),('Delivered','Delivered'),('Returned','Returned'),
                                                    ('Cancelled','Cancelled'),('Failed','Failed')])
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)

# Details for all orders made by users.
class OrderDetails(models.Model):
    order_details_id = models.CharField(max_length=15, primary_key=True)
    order_id = models.ForeignKey(Orders, default = None, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, default=None, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()