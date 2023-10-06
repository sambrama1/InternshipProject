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

def Log_out(request):
    logout(request)
    return redirect('signIn')


def homepage(request):
    return render(request,'homepage.html')

def select_table(request):
    table_1_occupied = Cart.objects.filter(table=1).exists()
    table_2_occupied = Cart.objects.filter(table=2).exists()
    table_3_occupied = Cart.objects.filter(table=3).exists()
    table_4_occupied = Cart.objects.filter(table=4).exists()
    # table_5_occupied = Cart.objects.filter(table=5).exists()
    # table_6_occupied = Cart.objects.filter(table=6).exists()
    # table_7_occupied = Cart.objects.filter(table=7).exists()
    # table_8_occupied = Cart.objects.filter(table=8).exists()
    # table_9_occupied = Cart.objects.filter(table=9).exists()
    # table_10_occupied = Cart.objects.filter(table=10).exists()
    
    available_tables = []
    if not table_1_occupied:
        available_tables.append(1)
    if not table_2_occupied:
        available_tables.append(2)
    if not table_3_occupied:
        available_tables.append(3)
    if not table_4_occupied:
        available_tables.append(4)       
    # if not table_5_occupied:
    #     available_tables.append(5)
    # if not table_6_occupied:
    #     available_tables.append(6)
    # if not table_7_occupied:
    #     available_tables.append(7)
    # if not table_8_occupied:
    #     available_tables.append(8)
    # if not table_9_occupied:
    #     available_tables.append(9)
    # if not table_10_occupied:
    #     available_tables.append(10)                            
    return render(request, 'tables.html', {'available_tables': available_tables})


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
                Dishes_instance = Dishes.objects.get(pk=dish_id)

                # Check if the user already has the same product in their cart for the selected table
                existing_cart_item = Cart.objects.filter(user=usr, dishes=Dishes_instance, table=table_instance).first()

                if existing_cart_item:
                    
                    existing_cart_item.quantity += 1
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
        user_cart = Cart.objects.filter(user=user,table=table_number)

        amount = 0
        tax = Decimal('0.05')
        total_amount = 0
        tax_amt = 0

        cart_items = []
        if user_cart:
            for cart_item in user_cart:
                temp_amount = cart_item.quantity * cart_item.dishes.price
                amount += temp_amount
                cart_items.append(cart_item)

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

            tax_amt = amount * tax
            total_amount = amount + tax_amt

        context = {
            'carts': cart_items,
            'amount': amount,
            'tax': tax_amt,
            'total': total_amount,
            'table_number': table_number,
        }
        return render(request, 'billpdf.html', context)
    else:
        return redirect('login')

def orderplaced(request):
    user = request.user

    amount = Decimal('0.0')
    tax = Decimal('0.05')
    total_amount = Decimal('0.0')
    

    dish_items = user.dish_set.all()
    for dp in dish_items:
        temp_amount = (dp.quantity * dp.product.price)
        amount += Decimal(temp_amount)      
   

    # Apply 20% discount on total_amount if it is over 2000
    if total_amount >= 2000:
        discount = total_amount * Decimal('0.2')
        total_amount -= discount

    context = {
        'Amount': amount,
        'Totalamount': total_amount,
        'dishitems': dish_items,
       
    }

    if orderplaced and request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = int('0')
        
        # Loop through each cart item and create an Orderedplaced object for each item
        for dish_item in dish_items:
            temp_amount = (dish_item.quantity * dish_item.product.price)
            amount += int(temp_amount)
           

            

            # Saving the order for each cart item
            Orderplaced.objects.create(
                User=user,
                product=dish_item.product,
                customerName=name,
                email=email,
                phone=phone,
                quantity=dish_item.quantity,
                amount=amount
            )

        # Delete cart items after all orders are placed
        dish_item.delete()
        return redirect('billpdf')

    return render(request, 'billpdf.html', context)



# -------------Orders page to show the all ordered items for particular user -----------------#

def orders(request):
    myOrders = Orderplaced.objects.filter(User=request.user)
    return render(request, 'billpdf.html',{})


# -------------Search function to search the items -----------------#

def search_view(request):
    search = request.GET.get('search')
    results = None

    if search:
        # Perform the search query using the product model 
        results = cart.objects.filter( Q(name__icontains = search) |  Q(category__icontains = search) ) # Search by product name or category 


    context = {
        'search': search,
        'results': results,
    }

    return render(request, 'search.html', context)


def cancel_order(request, order_id):
    try:
        order = Orderplaced.objects.get(pk=order_id)

        # Check if the order status is not 'Delivered'
        if order.status != 'Delivered':
            # Update the order status to 'cancel'
            order.status = 'Canceled'
            order.save()

    except Orderplaced.DoesNotExist:
        print("There is no ---Orderplaced--- model or table in ur database...")

    return redirect('billpdf')            
