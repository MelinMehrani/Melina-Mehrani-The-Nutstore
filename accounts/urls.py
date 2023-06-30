from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views as accounts_views

# app_name = 'accounts'

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')), #to use the default templates for reseting the password
    # path('login/', accounts_views.login_view, name='login'), #urls for the views we've created
    # path('logout/', accounts_views.logout_view, name='logout'),
    # path('signup/', accounts_views.signup_view, name='signup'),
    path('signup/', accounts_views.SignUpView.as_view(), name='signup'),
    path('change-password/', accounts_views.change_password, name='change_password'),
    #the following url patterns are for the built-in Django authentication views for password reset functionality.
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]