from django.db import models
from shop.models import *
from django.contrib.auth.models import User
from accounts.models import Address 

class CartList(models.Model):
    cart_id=models.CharField(max_length=250,unique=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cart_id
    
class Items(models.Model):
    prodt=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(CartList,on_delete=models.CASCADE)
    quan=models.IntegerField()
    active=models.BooleanField(default=True)
    def total(self):
        return self.prodt.price * self.quan
    def __str__(self):
        return self.prodt.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    order_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
