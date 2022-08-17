from django.contrib import admin
from .models import Product, Category, Message, User , Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(User)