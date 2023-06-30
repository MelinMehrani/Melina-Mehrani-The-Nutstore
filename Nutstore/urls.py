from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

#app_name = 'warehouse' #Do we really need this?

urlpatterns = [
    path('', views.home, name='home'), #homeUrl
    path('category/<str:category>/', views.category_products, name='category'), #categoryproducts url pattern
    path('profile/', views.profile, name='profile'), #Profile Url
    path('product/addtocart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), #add the item to cart url pattern
    path('cart/', views.cart, name='cart'), #users cart where chosen items are listed url pattern
    path('cart/<int:cart_item_id>/remove/', views.remove_from_cart, name='remove_from_cart'), #to remove items from cart
    path('cart/<int:cart_item_id>/update/', views.update_cart, name='update_cart'), #update weights in cart
    path('cart/purchase-confirmation/', views.purchase_confirmation, name='purchase_confirmation'), #purchase confirmation url pattern
    path('admin_panel/', views.admin_panel, name='admin_panel'),  #THE ADMIN PANEL PAGE URL PATTERN
    path('admin_panel/manage_products/', views.manage_products, name='manage_products'), #MANAGE PRODUCTS BY ADMIN URL PATTERN 
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),  #EDIT THE PRODUCT BY ADMIN
    path('add-product/', views.add_product, name='add_product'),   #ADD NEW PRODUCTS BY ADMIN
    path('admin_panel/preview_orders/', views.preview_orders, name='preview_orders'),   #LIST ALL ORDERS FOR ADMIN
    path('orders/<int:order_id>/', views.order_status, name='order_status'),  #ORDER DETAILS FOR ADMIN TO CHANGE ORDER STATUS
    path('admin_panel/manage_warehouses/', views.manage_warehouses, name='manage_warehouses'), #LIST ALL WAREHOUSES FOR ADMIN
    path('warehouse/<int:warehouse_id>/', views.warehouse_detail, name='warehouse_detail'), #Warehouse Details Url pattern
    path('create_warehouse/', views.create_warehouse, name='create_warehouse'), #createwarehouse url pattern
    path('city/add/', views.city_add, name='city_add'),                 #add cities
    path('edit_warehouse/<int:warehouse_id>/', views.edit_warehouse, name='edit_warehouse'), #edit warehouse page
    path('about/', views.AboutPageView.as_view(), name='about'),   #about page
    path('contact/', views.ContactPageView.as_view(), name='contact'),   #contact us page
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/', LoginView.as_view(template_name='warehouse/login.html'), name='login'),
    #path('accounts/logout/', LogoutView.as_view(), name='logout'),
]