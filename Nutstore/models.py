from django.db import models
#from accounts.models import CustomUser


#City table
class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Warehouse table
class Warehouse(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length = 500)

    def __str__(self):
        return self.name

#Products table
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('pistachio', 'Pistachio'),
        ('almond', 'Almond'),
        ('cashew', 'Cashew'),
        ('peanuts', 'Peanuts'),
        ('confectioneries', 'Confectioneries'),
        ('dried fruits', 'Dried Fruits'),
        ('snacks', 'Snacks'),
        ('other', 'Other Products'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits = 10, decimal_places = 2) #added  #PAY ATTENTION MEL!: I have changed this from quantity to stock, MAKE SURE TO CHECK AND CHANGE THE NECESSARY THINGS
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    image = models.URLField(blank=True)
    #image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

#The products that a warehouse has. We write this in order to prevent deleting a whole product when we only want to delete forexample a product in one warehouse.
# class WarehouseProduct(models.Model):
#     warehouseid = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     productid = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return self.name
    
# class Buyer(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username


#from .buyer import Buyer
#from .product import Product

# class Order(models.Model):
#     buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
#     #product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product)
#     quantity = models.IntegerField()
#     ordered_at = models.DateTimeField(auto_now_add=True)
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     def __str__(self):
#         return f"{self.buyer.user.username} - {self.products.name} ({self.quantity})"
#     #def __str__(self):
#         #return f"Order #{self.pk}"


#THE MODEL FOR SHOPPING CART:
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)    #this actually allows us to have a weight up to 999999.99


#new order model:
class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing') 

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    

# class OrderItem(models.Model):
#     name = models.CharField(max_length=200, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order)