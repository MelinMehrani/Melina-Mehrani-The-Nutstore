from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views as accounts_views



urlpatterns = [
    path('signup/', accounts_views.SignUpView.as_view(), name='signup'),
    path('change-password/', accounts_views.change_password, name='change_password'),
]