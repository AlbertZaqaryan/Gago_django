from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", {'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

class HomeListView(ListView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

class ShopListView(ListView):
    template_name = 'shop.html'

    def get(self, request):
        shops = Product.objects.all()
        return render(request, self.template_name, {'shops':shops})

def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('id'))
            product_check = Product.objects.get(id=prod_id)

            if product_check:
                if not Order.objects.filter(user_id=request.user.id):
                    Order.objects.create(user_id=request.user.id)
                order = Order.objects.get(user_id=request.user.id).id
                if OrderProduct.objects.filter(user_id=request.user.id, product_id=prod_id):
                    order_qty = OrderProduct.objects.get(product_id=prod_id, user_id=request.user.id).quantity
                    OrderProduct.objects.filter(product_id=prod_id).update(quantity=order_qty + 1)
                    return JsonResponse({'status': 'Product updated successfully'})
                else:
                    OrderProduct.objects.create(user_id=request.user.id, product_id=prod_id,
                                                price=Product.objects.get(pk=prod_id).price,
                                                quantity=1, order_id=order)
                    return JsonResponse({'status': 'Product added successfully'})

            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Login to Continue'})
    return JsonResponse({'error': 'Login to Continue'}, status=422)


def cart_quantity_update(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        if OrderProduct.objects.filter(user_id=request.user.id, product_id=product_id):
            order_qty = int(request.POST.get('quantity'))
            orderproduct = OrderProduct.objects.get(product_id=product_id, user_id=request.user.id)
            orderproduct.quantity = order_qty
            orderproduct.save()
            total_price = order_qty * OrderProduct.objects.get(user_id=request.user.id, product_id=product_id).price
            return JsonResponse({'status': 'Updated Successfully', 'total': total_price}, status=200)
        return JsonResponse({'status': 'Error'}, status=422)
    return JsonResponse({'status': 'Error'}, status=422)


def cart_quantity_delete(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        if OrderProduct.objects.filter(user_id=request.user.id, product_id=product_id):
            orderproduct = OrderProduct.objects.get(product_id=product_id, user_id=request.user.id)
            product = Product.objects.get(pk=product_id)
            orderproduct.delete()
            return JsonResponse({'status': product.name + ' Successfully Deleted'}, status=200)
        return JsonResponse({'status': 'Error'}, status=422)
    return JsonResponse({'status': 'Error'}, status=422)


def cartview(request):
    cart = OrderProduct.objects.filter(user_id=request.user)
    order = Order.objects.get(user_id=request.user)
    orderproduct = order.orderproduct_set.all()
    context = {
        'cart': cart,
        'orderproducts': orderproduct,
        'order': order,
    }
    return render(request, 'cart.html', context)