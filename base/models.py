
from email.mime import image
from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
    username = models.CharField(max_length=200,unique=True,default='Anonymous')
    email = models.EmailField(null=True,unique=True)
    bio = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    descritpion = models.TextField(max_length=500,null=True,blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL , null=True)
    image = models.ImageField(null=True, default='Product.png')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE , primary_key=True)
    product = models.ManyToManyField(Product)

class Message(models.Model):
    body = models.TextField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body



