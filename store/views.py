from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm

def list(request):
    prods = Product.objects.all().order_by('pr_type')
    user = request.user
    return render(request, 'store/list.html', {'prods' : prods, 'user' : user})

def prod_detail(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    return render(request, 'store/prod_detail.html', {'prod': prod})

@transaction.atomic
def create_client(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST['password'])
            user = user_form.save()
            client = Client.objects.get(user_id = user.id)
            user.client.full_name=request.POST['full_name']
            user.client.gender = request.POST['gender']
            user.client.address = request.POST['address']
            user.client.bank_card_id = request.POST['bank_card_id']
            user.client.phone_number = request.POST['phone_number']
            user.client.status = 'Новый'
            user.client.save()
            messages.success(request, ('Ваш профиль был успешно создан!'))
            return redirect('list')
        else:
            messages.error(request, ('Возникла ошибка.'))
    else:
        user_form = UserForm()
        client_form = ClientForm()
    return render(request, 'registration/add_user.html', {
        'user_form': user_form,
        'client_form': client_form
    })

def authent(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        print (form.is_valid(), form.errors, type(form.errors))
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list')
            else:
                messages.error(request, ('Возникла ошибка.'))
        else:
            messages.error(request, ('Возникла ошибка.'))
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {
        'form': form
    })

def order_new(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_id = request.user.client
            pr = Product.objects.get(pk=request.POST['prod_id'])
            order.prod_id = pr
            price = pr.price
            order.sum_total = price
            order.save()
            return redirect('list')
    else:
        form = OrderForm()
    return render(request, 'store/order_new.html', {'form': form})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

def get_orders(request):
    client = request.user.client
    orders = Order.objects.filter(client_id = client)
    products = []
    for o in orders:
        products.append(Product.objects.get(id=o.prod_id.id))
    return render(request, 'store/orders.html', {'client': client, 'orders': orders, 'products': products})