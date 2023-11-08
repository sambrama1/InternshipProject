from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import *
from decimal import Decimal
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from copy import deepcopy

def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('cnfpassword')

        if confirmpassword != password:
            return HttpResponse("Your Password and Comfirm Paassword are not matching")
        else:
            my_user = User.objects.create_user(username,email,password)
            my_user.save()
            return redirect('menu')
    return render(request,'register.html')


def logn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('menu')
        else:
            return HttpResponse("username & password is incorrect!!!")
        
    return render(request,'login.html')

def log_out(request):
    logout(request)
    return redirect('/')


def homepage(request):
    return render(request,'homepage.html')

@login_required(login_url='login')
def select_table(request):
    table_1_occupied = Cart.objects.filter(table=1).exists()
    table_2_occupied = Cart.objects.filter(table=2).exists()
    table_3_occupied = Cart.objects.filter(table=3).exists()
    table_4_occupied = Cart.objects.filter(table=4).exists()
    
    available_tables = []
    if not table_1_occupied:
        available_tables.append(1)
    if not table_2_occupied:
        available_tables.append(2)
    if not table_3_occupied:
        available_tables.append(3)
    if not table_4_occupied:
        available_tables.append(4)                         
    return render(request, 'tables.html', {'available_tables': available_tables})

@login_required(login_url='login')
def menu(request):
    table_number = request.GET.get('table')
    print(table_number,'-----------------------------------------')
    if not table_number:
        return redirect('tables')
    
    Baverages = Dishes.objects.filter(category='Baverages')
    south = Dishes.objects.filter(category='South Indians')

    context = {
        'south': south,
        'Baverages': Baverages,
        'table_number': table_number,
    }
    return render(request, 'menu.html', context)


def addToCart(request):
    if request.method == 'GET':
        dish_ids = request.GET.getlist('dish_ids[]') 
        table_number = request.GET.get('table')
        print(dish_ids,table_number)

        if not dish_ids or not table_number:
           
            return HttpResponse("Invalid request")

        # Check if the user is authenticated 
        if request.user.is_authenticated:
            
            usr = request.user
            
            table_instance, created = Table.objects.get_or_create(table_number=table_number)

           
            for dish_id in dish_ids:
                print('dishid',dish_id)
                Dishes_instance = Dishes.objects.get(pk=dish_id)
                print(Dishes_instance)
                # Check if the user already has the same product in their cart for the selected table
                existing_cart_item = Cart.objects.filter(user=usr, dishes=Dishes_instance, table=table_instance).first()
                print(existing_cart_item)
                if existing_cart_item:
                    existing_cart_item.save()
                else:
                    
                    new_cart_item = Cart(user=usr, dishes=Dishes_instance, table=table_instance)
                    new_cart_item.save()

       
        cart_url = reverse('cart')  
        cart_url_with_params = f"{cart_url}?table={table_number}"
        return HttpResponseRedirect(cart_url_with_params)



def cart(request):
    if request.user.is_authenticated:
        table_number = request.GET.get('table')
        print('cart --------', table_number)
        if not table_number:
            return redirect('tables')

        user = request.user
        user_cart = Cart.objects.filter(user=user, table=table_number)

        amount = 0
        tax = Decimal('0.05')
        total_amount = 0
        tax_amt = 0

        cart_items = []
        if user_cart:
            for cart_item in user_cart:
                temp_amount = cart_item.quantity * cart_item.dishes.price
                amount += temp_amount
                # Create a new Cart object with the same attributes and values
                cart_copy = deepcopy(cart_item)
                cart_items.append(cart_copy)

            tax_amt = amount * tax
            total_amount = amount + tax_amt

        context = {
            'carts': cart_items,
            'amount': amount,
            'tax': tax_amt,
            'total': total_amount,
            'table_number': table_number,
        }
        return render(request, 'cart.html', context)
    else:
        return redirect('login')



def minusCart(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        table_number = request.POST.get('table_number')
        print(dish_id)
        print(dish_id)
        print(table_number)
        print(table_number)
        c = Cart.objects.get(dishes=dish_id,user=request.user,table = table_number)

        c.quantity -= 1
        c.save()

        amount = Decimal('0.0') 
        total_amount = Decimal('0.0') 

        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            temp_amount = p.quantity * p.dishes.price
            amount += Decimal(temp_amount)

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount,
            'table_number':table_number,
        }
        return JsonResponse(data)
    
def plusCart(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        table_number = request.POST.get('table_number')
        print('table------',table_number)
        print(dish_id)
        print(dish_id)
        print(table_number)
        print(table_number)
        c = Cart.objects.get(dishes=dish_id,user=request.user,table = table_number)
        c.quantity += 1
        c.save()

        amount = Decimal('0.0') 
        total_amount = Decimal('0.0') 

        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            temp_amount = p.quantity * p.dishes.price
            amount += Decimal(temp_amount)

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount,
            'table_number':table_number,
        }
        return JsonResponse(data)
    
def removeCart(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        table_number = request.POST.get('table_number')
        print(dish_id)
        print(table_number)

        c = Cart.objects.get(dishes=dish_id,user=request.user,table = table_number)
        c.delete()

        amount = Decimal('0.0')  
        total_amount = Decimal('0.0')  

        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            temp_amount = p.quantity * p.dishes.price
            amount += Decimal(temp_amount)
        

        data = {
            'amount': amount,
            'totalamount': total_amount,
            'table_number':table_number,
        }
        return JsonResponse(data)   


def bill(request):
    if request.user.is_authenticated:
        table_number = request.GET.get('table')
        print(table_number)
        if not table_number:
            return redirect('tables')

        user = request.user
        user_cart = Cart.objects.filter(user=user, table=table_number)

        amount = 0
        tax = Decimal('0.05')
        total_amount = 0
        tax_amt = 0

        cart_items = []
        table_instance = Table.objects.get(table_number=table_number)
        if user_cart:
            for index, cart_item in enumerate(user_cart, start=1):
                temp_amount = cart_item.quantity * cart_item.dishes.price
                amount += temp_amount
                cart_items.append({
                    'index': index,
                    'name': cart_item.dishes.name,
                    'amount': cart_item.dishes.price,
                    'quantity': cart_item.quantity,
                    'total_price': temp_amount
                })
                dish_instance = Dishes.objects.get(name=cart_item.dishes.name)

                order = Orderplaced.objects.create(
                    user = user,
                    table = table_instance,
                    dishes = dish_instance,
                    quantity = cart_item.quantity,
                    amount = amount,  
                )
                order_date = order.Ordered_date.date
                print(order_date)
            tax_amt = amount * tax
            total_amount = amount + tax_amt

        order_date: Orderplaced.objects.filter(table= table_instance,)
        context = {
            'carts': cart_items,
            'amount': amount,
            'tax': tax_amt,
            'total': total_amount,
            'table_number': table_number,
            'date': order_date
        }

            # Delete cart items after all orders are placed
        for cart_item in user_cart:
            cart_item.delete()

        return render(request, 'billpdf.html', context)
    else:
        return redirect('login')

