from django.shortcuts import render , redirect
from .models import Product, Category , Message , Cart
from .form import MyUserCreationForm , Productform
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate , login , logout 
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method == 'GET':
        q = request.GET.get('q','')
        products = Product.objects.filter(category__name__icontains = q)
    elif request.method == 'POST':
        q = request.POST.get('q','')
        products = Product.objects.filter(name__icontains = q)
    category  = Category.objects.all()
    content = {'category':category , 'products':products}
    return render(request, 'index.html', content)

def product_page(request,pk):
    product = Product.objects.get(id=pk)
    messages = Message.objects.filter(product=product)

    if request.method == 'POST':
        body = request.POST.get('body')
        message = Message(user=request.user, product = product, body = body)
        message.save()
     
    product = Product.objects.get(id=pk)
    messages = Message.objects.filter(product=product)
    content = {'product': product, 'p_messages':messages}
    return render(request, 'product.html' , content)

def createproduct(request):
    form  = Productform()
    if request.method == "POST":
        category_name = request.POST.get('category')
        category , created  = Category.objects.get_or_create(name=category_name)
        seller = request.user
        name = request.POST.get('name')
        description = request.POST.get('descritpion')
        stock = request.POST.get("stock")
        price = request.POST.get('price')
        image = request.FILES.get('image')
        Product.objects.create(name=name,seller=seller,category=category,descritpion=description,stock=stock,price=price,image=image)

    product = Product.objects.all()
    categories = Category.objects.all()
    content = {'form':form , 'product':product,'categories':categories}
    return render(request,'product_form.html',content)

def editproduct(request , pk):
    product  = Product.objects.get(id=pk)
    form = Productform(instance=product) # This prefills the RoomForm class with room data 

    if request.user != product.seller:
        return HttpResponse(f"This room can be only edited by {product.seller}." )

    if request.method == "POST":
        category_name = request.POST.get('category')
        category , created  = Category.objects.get_or_create(name=category_name)
        product.seller = request.user
        product.name = request.POST.get('name')
        product.description = request.POST.get('descritpion')
        product.stock = request.POST.get("stock")
        product.price = request.POST.get('price')
        product.image  = request.FILES.get('image')
        product.category = category
        product.save()
        return redirect("home")

    content = {"form" : form , 'product' : product,}
    return render(request , "product_form.html" , content)

def deleteproduct(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('home')
    content = {'content':product}
    return render(request, 'delete.html',content)


def loginpage(request):
    page = 'login'
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            
            
            return redirect('home')
        else:
            messages.error(request , 'Email or Password is incorrect')

    content = {'page':page}
    return render(request,'login.html',content)

def registerpage(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)

            user.username = user.username.lower()
            user.save()
            cart = Cart(user = user)
            cart.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'login.html' , {'form' : form})

def logoutpage(request):
    logout(request)
    return redirect('home')

def Addcart(request,pk):
    user = request.user
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(user=user)
    cart.product.add(product)
    return redirect('home')

def Cartitem(request):
    
    cart = Cart.objects.get(user = request.user)
    products = Product.objects.filter(cart = cart)
    content = {'products':products}
    return render(request,'cart.html',content)

def deleteitem(request,pk):
    user = request.user
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(user=user)
    cart.product.remove(product)
    return redirect('home')

def checkout(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        user = request.user
        product = Product.objects.get(id=pk)
        cart = Cart.objects.get(user=user)
        cart.product.remove(product)

        # email
        name = request.user
        email = request.user.email
        body = "Your Purchase has been made! You'll recieve your order soon." + " Your purchased item: " + product.name
        send_mail(
            name,
            body,
            'surubasnet824@gmail.com', # sender email
            [email], # receiver email
            fail_silently=False,
        )

        return render(request,'Thankyou.html')
    content = {'product':product}
    return render(request,'checkout.html',content)