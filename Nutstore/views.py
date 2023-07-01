from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import City, Warehouse, Product, Order, CartItem
from .forms import WarehouseForm, OrderStatusForm, ProductForm, CityForm
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Sum
from django.views.generic import TemplateView

User = get_user_model()
#HomePageView
#extracting the unique categories of products from the database and passing them to the home.html template via the context dictionary
def home(request):
    cities = City.objects.all()
    categories = set(product.category for product in Product.objects.all())
    context = {'categories': categories, 'cities': cities}
    return render(request, 'home.html', context)

#PRODUCTS OF A CATEGORY PAGE VIEW
#category view that fetches all the products for a given category and passes them to a categoryproducts.html template
@login_required
def category_products(request, category):
    categories = set(product.category for product in Product.objects.all())
    user_city = ''
    if request.user.is_authenticated:     #filters the products based on user's city, if not logged in shows all the products
        try:
            user = request.user
            #user_profile = user.objects.get(email=request.user.email)
            user_city = user.city
        except CustomUser.DoesNotExist:
            pass
        
    #We group the same products from different warehouses in city by their name cause the users don't need to see same products but from different warehouses
    products = Product.objects.filter(category=category, warehouse__city=user_city) \
    .values('name', 'category', 'id', 'description', 'image', 'price') \
    .annotate(total_stock=Sum('stock')) \
    .order_by('name')
    print(products)
    context = {'category': category, 'products': products, 'categories': categories}
    return render(request, 'categoryproducts.html', context)

# def category_products(request, category):
#     user_city = None
#     if request.user.is_authenticated:  #filters the products based on user's city, if not logged in shows all the products
#         try:
#             user = get_user_model()
#             user_profile = user.objects.get(email=request.user.email)
#             user_city = user_profile.city
#         except CustomUser.DoesNotExist:
#             pass
#     products = Product.objects.filter(category=category, warehouse__city=user_city)
#     context = {'category': category, 'products': products}
#     return render(request, 'categoryproducts.html', context)



#ProfilePageView
#Retrives the current user and all the orders this user has made
@login_required
def profile(request):
    categories = set(product.category for product in Product.objects.all())
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'categories': categories,
        'user': user,
        'orders': orders,
    }
    return render(request, 'profile.html', context)





#ADDING ITEMS TO SHOPPING CART VIEW:
@login_required  #if the user is not authenticated, will be redirected to login page and can't add an item without authentication to cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    print(request.method)
    if request.method == 'POST' :
        weight = request.POST.get('weight')
        
        if user.is_seller:        #WHOLESOME BUYERS WILL HAVE THE WEIGHTS IN KILOGRAM
            weight_unit = 'kg'
        else:
            weight_unit = 'g'     #ORDINARY BUYERS WILL HAVE THE WEIGHTS IN GRAMS AS THEY PURCHASE IN LOWER AMOUNTS
            weight = float(weight) / 1000.0
        total_weight = float(weight)
        # create a new cart item
        cart_item_weight = float(weight)
        cart_item = CartItem.objects.create(product=product, user=user, weight=cart_item_weight)
        cart_item.save()
        available_stock = 0
        preferred_warehouses = Warehouse.objects.filter(city=user.city).order_by('id')
        # check the stock levels of the warehouses in order of their ID
        for warehouse in preferred_warehouses:
            try:
                p = Product.objects.get(id=product_id, warehouse=warehouse)
                available_stock = p.stock
                total_weight -= float(available_stock)
                if total_weight< 0 : #available_stock >= total_weight:
                    break
                
                    
            except Product.DoesNotExist:
                pass

        # check if there is enough stock for the requested weight
        if total_weight > 0:
            return HttpResponse('Error: not enough stock available.')
       #This will ensure that the warehouses are checked in the order of their ID when we loop over them to find the warehouse with enough stock to fulfill the requested weight.
        # Redirect the user back to the previous page
        return redirect (str(reverse_lazy('category', args= (product.category,))))
    
    return render(request , 'add_to_cart.html', {'product' : product})
    

    
    

    

    

    

#PREVIOUS ADD_TO_CART
# @login_required  #if the user is not authenticated, will be redirected to login page and can't add an item without authentication to cart
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     weight = request.POST.get('weight')
#     user = request.user

#     if user.is_seller:      #WHOLESOME BUYERS WILL HAVE THE WEIGHTS IN KILOGRAM
#         weight_unit = 'kg'
#     else:                   #ORDINARY BUYERS WILL HAVE THE WEIGHTS IN GRAMS AS THEY PURCHASE IN LOWER AMOUNTS
#         weight_unit = 'g'
#         # convert weight from grams to kilograms
#         weight = float(weight) / 1000.0

#     # calculate the total weight in kilograms
#     total_weight = float(weight)

#     # get the total stock of the product in the user's city
#     city_stock = Decimal('0')
#     warehouses = Warehouse.objects.filter(city=user.city)
#     for warehouse in warehouses:
#         try:
#             product_stock = Product.objects.get(id=product_id, warehouse=warehouse).stock
#             city_stock += product_stock
#         except Product.DoesNotExist:
#             pass

#     # check if there is enough stock for the item
#     if total_weight > city_stock:
#         return HttpResponse('Error: not enough stock available.')

#     # create a new cart item
#     cart_item = CartItem.objects.create(product=product, user=user, weight=total_weight)
#     cart_item.save()

#     # Redirect the user back to the previous page
#     return redirect(request.META.get('HTTP_REFERER'))



#THE SHOPPING CART WHERE ALL THE CHOSEN ITEMS BY THE USERS IS VIEWED
@login_required
def cart(request):
    categories = set(product.category for product in Product.objects.all())
    user = request.user
    cart_items = CartItem.objects.filter(user=user, is_active=True)
    total_cost = sum([(item.product.price * item.weight) for item in cart_items])
    context = {'cart_items': cart_items, 'total_cost': total_cost, 'categories': categories}
    return render(request, 'cart.html', context)

#TO REMOVE ITEMS FROM THE CART
@login_required
def remove_from_cart(request, cart_item_id):
    user = request.user
    cart_item = CartItem.objects.get(id=cart_item_id, user=user)
    cart_item.delete()
    return redirect('cart')

#WHEN THE USER CHANGES THE AMOUNT IN THE CART PAGE
#we check stock availability again
@login_required
def update_cart(request, cart_item_id):

    user = request.user
    cart_item = CartItem.objects.get(id=cart_item_id, user=user)
    old_weight = cart_item.weight
    new_weight = float(request.POST['weight'])
    
    cart_item.weight = new_weight
    cart_item.save()
    

    # check the stock availability again
    product = cart_item.product
    preferred_cities = [user.city]
    available_stock = 0
    total_weight = new_weight
    
    preferred_warehouses = Warehouse.objects.filter(city=user.city).order_by('id')
    
        # check the stock levels of the warehouses in order of their ID
    for warehouse in preferred_warehouses:
        try:
                p = Product.objects.get(id=product.id, warehouse=warehouse)
                available_stock = p.stock
                total_weight -= float(available_stock)
                if total_weight< 0 : #available_stock >= total_weight:
                    break
                
                    
        except Product.DoesNotExist:
                pass
    # for city in preferred_cities:
    #     warehouses = Warehouse.objects.filter(city=city).order_by('id')
    #     for warehouse in warehouses:
    #         try:
    #             p = Product.objects.get(id=product.id, warehouse=warehouse)
    #             available_stock = p.stock
    #             if available_stock >= total_weight:
    #                 break
    #             else:
    #                 total_weight -= available_stock
    #         except Product.DoesNotExist:
    #             pass
    # if available_stock >= total_weight:
    #     break

    # if there is not enough stock, revert the weight change and return an error message
    if total_weight > 0:
        cart_item.weight = old_weight
        cart_item.save()
        return HttpResponse('Error: not enough stock available.')

    return redirect('cart')

#previous update cart 
# @login_required
# def update_cart(request, cart_item_id):
#     user = request.user
#     cart_item = CartItem.objects.get(id=cart_item_id, user=user)
#     cart_item.weight = float(request.POST['weight'])
#     cart_item.save()
#     return redirect('cart')


#THE PURCHASE CONFIRMATION VIEW AFTER SUBMITTING THE ORDERS
@login_required
def purchase_confirmation(request):
    user = request.user
    categories = set(product.category for product in Product.objects.all())
    # retrieve the user's cart items and calculate the total cost
    cart_items = CartItem.objects.filter(user=user, is_active=True)
    total_cost = sum([item.product.price * item.weight for item in cart_items])

    # create a new order
    order = Order.objects.create(user=user, total_cost=total_cost)
    for item in cart_items:
        order.items.add(item)
        item.is_active = False
        item.save()
    order.save()

    # update the stock level of the product in the warehouse where the purchase was made
    for item in cart_items:
        product = item.product
        weight = item.weight
        warehouse = product.warehouse

        # subtract the weight of the item from the stock level of the product in the warehouse where the purchase was made
        if warehouse.city == user.city:
            p = Product.objects.get(id=product.pk, warehouse=warehouse)
            p.stock -= weight
            p.save()

    # # delete the user's cart items
    # cart_items_delete = CartItem.objects.filter(user=user, is_active=True)
    # cart_items_delete.delete()

    # redirect the user to the order confirmation page
    return render(request, 'purchase_confirmation.html', {'order': order, 'categories': categories})

#previous purchase confirmation view
# @login_required
# def purchase_confirmation(request):
#     user = request.user

#     # retrieve the user's cart items and calculate the total cost
#     cart_items = CartItem.objects.filter(user=user, is_active=True)
#     total_cost = sum([item.product.price * item.weight for item in cart_items])

#     # create a new order
#     order = Order.objects.create(user=user, total_cost=total_cost)

#     # update the stock levels of the warehouses
#     for item in cart_items:
#         warehouse = item.product.warehouse
#         product = item.product
#         weight = item.weight

#         # subtract the weight of the item from the stock level of the product in the warehouse
#         product_stock = product.stock - weight
#         Product.objects.filter(id=product.id, warehouse=warehouse).update(stock=product_stock)

#     # redirect the user to the order confirmation page
#     return render(request, 'purchase_confirmation.html', {'order': order})



#ADMIN PANEL
@login_required
@user_passes_test(lambda u: u.is_superuser)   #this makes sure only superusers get access to this page
def admin_panel(request):
    categories = set(product.category for product in Product.objects.all())
    return render(request, 'admin_panel/admin_panel.html', {'categories': categories})

#MANAGE PRODUCTS (LIST OF PRODUCTS)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_products(request):
    products = Product.objects.all()
    categories = set(product.category for product in Product.objects.all())
    # Get filter parameters from request
    category = request.GET.get('category')
    city = request.GET.get('city')
    warehouse = request.GET.get('warehouse')

    # Apply filters if they exist
    if category:
        products = products.filter(category=category)
    if city:
        products = products.filter(warehouse__city=city)
    if warehouse:
        products = products.filter(warehouse=warehouse)

    context = {
        'products': products,
        'category_choices': Product.CATEGORY_CHOICES,
        'cities': Warehouse.objects.values_list('city', flat=True).distinct(),
        'warehouses': Warehouse.objects.all(),
        'category_filter': category,
        'city_filter': city,
        'warehouse_filter': warehouse,
        'categories': categories
    }
    return render(request, 'admin_panel/manage_products.html', context)

#EDIT PRODUCTS
@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, pk):
    categories = set(product.category for product in Product.objects.all())
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'admin_panel/edit_product.html', context)

#ADD PRODUCTS BY ADMIN
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    categories = set(product.category for product in Product.objects.all())
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_products')

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'admin_panel/add_product.html', context)



#PREVIEW ORDERS IN LIST FOR ADMIN
@login_required
@user_passes_test(lambda u: u.is_superuser)
def preview_orders(request):
    categories = set(product.category for product in Product.objects.all())
    order_id_query = request.GET.get('order_id')
    if order_id_query:
        orders = Order.objects.filter(id=order_id_query).order_by('-created_at')   #This is for the search by id
    else:
        orders = Order.objects.all().order_by('-created_at')    #if there is no id filter then gets all order objects and lists them based on their creation date

    context = {
        'orders': orders,
        'order_id_query': order_id_query,
        'categories': categories
    }
    return render(request, 'admin_panel/preview_orders.html', context)

#ORDER DETAILS
#THIS IS THE VIEW FOR THE SUPERUSER TO CHANGE THE STATUS OF EACH ORDER WHEN DELIVERED
@user_passes_test(lambda u: u.is_superuser)
def order_status(request, order_id):
    categories = set(product.category for product in Product.objects.all())
    # Retrieve the Order object for the selected order ID
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully.')
            return redirect('order_status', order_id=order.id)
    else:
        form = OrderStatusForm(instance=order)
    context = {
        'order': order,
        'form': form,
        'categories': categories
    }
    return render(request, 'admin_panel/order_status.html', context)


#MANAGE WAREHOUSES PAGE FOR ADMIN
#LISTS ALL WAREHOUSES
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_warehouses(request):
    categories = set(product.category for product in Product.objects.all())
    # Retrieve all warehouses
    warehouses = Warehouse.objects.all()

    # Filter warehouses by city if a city is chosen
    city = request.GET.get('city', None)
    if city:
        warehouses = warehouses.filter(city__iexact=city)

    # Search warehouses by ID if searched
    search = request.GET.get('search', None)
    if search:
        warehouses = warehouses.filter(id__icontains=search)

    context = {
        'warehouses': warehouses,
        'categories': categories
    }
    return render(request, 'admin_panel/manage_warehouses.html', context)


#AddWarehousePageView
@user_passes_test(lambda u: u.is_superuser)    
def create_warehouse(request):
    categories = set(product.category for product in Product.objects.all())
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_warehouses')    #if the form is valid then it will be saved and the user will be redirected to manage_warehouses page
    else:
        form = WarehouseForm()
    return render(request, 'admin_panel/create_warehouse.html', {'form': form, 'categories': categories})

#ADD CITY PAGE VIEW
@user_passes_test(lambda u: u.is_superuser)
def city_add(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save()
            return redirect('create_warehouse')
    else:
        categories = set(product.category for product in Product.objects.all())
        form = CityForm()
    return render(request, 'admin_panel/city_add.html', {'form': form, 'categories': categories})

#WAREHOUSE DETAIL PAGE VIEW
@user_passes_test(lambda u: u.is_superuser)
def warehouse_detail(request, warehouse_id):
    categories = set(product.category for product in Product.objects.all())
    # Retrieve the Warehouse object for the selected warehouse ID
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    products = Product.objects.filter(warehouse=warehouse)
    return render(request, 'admin_panel/warehouse_detail.html', {'warehouse': warehouse, 'products': products, 'categories': categories})

#EDIT WAREHOUSE PAGE
@user_passes_test(lambda u: u.is_superuser)
def edit_warehouse(request, warehouse_id):
    categories = set(product.category for product in Product.objects.all())
    # Retrieve the Warehouse object for the selected warehouse ID
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        # If the form has been submitted, validate the data and save the changes
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse_detail', warehouse_id=warehouse.id)
    else:
        # If the form has not been submitted, create a new form instance with the current warehouse data
        form = WarehouseForm(instance=warehouse)

    context = {
        'warehouse': warehouse,
        'form': form,
        'categories': categories
    }
    return render(request, 'admin_panel/edit_warehouse.html', context)

class AboutPageView(TemplateView):
    template_name = 'about.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'