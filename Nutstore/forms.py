from django.forms import ModelForm, ModelChoiceField
from .models import Product, Order, Warehouse, City
from django import forms

#ADD CITY FORM
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

#form that is used to create an HTML form for creating or editing a Warehouse object
class WarehouseForm(ModelForm):
    class Meta:
        model = Warehouse
        fields = ['city', 'name', 'location']

#THIS IS THE FORM FOR THE ADMIN TO SET THE STATUS
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        labels = {
            'status': 'Order Status'
        }
        widgets = {
            'status': forms.Select(choices=Order.STATUS_CHOICES)   
        }


#PRODUCT FORM FOR ADDING OR EDITING PRODUCTS BY ADMIN
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'warehouse', 'stock', 'category', 'image']