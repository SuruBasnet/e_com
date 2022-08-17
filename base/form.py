from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import  User ,Product


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','status', 'password1','password2']

class Productform(ModelForm):
    class Meta:
        model = Product
        fields = ['name','descritpion','category','image','stock','price']