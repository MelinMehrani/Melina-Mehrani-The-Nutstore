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
    stock = models.DecimalField(max_digits = 10, decimal_places = 3) 
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    image = models.URLField(blank=True)
    #image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name



#THE MODEL FOR SHOPPING CART:
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=9, decimal_places=3)    #this actually allows us to have a weight up to 999999.99
    is_active = models.BooleanField(default=True)


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
    
