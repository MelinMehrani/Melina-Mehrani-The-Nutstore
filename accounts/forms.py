from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser



  
class SignUpForm(UserCreationForm): 
      
     class Meta(UserCreationForm):  
         model = CustomUser  
         fields = UserCreationForm.Meta.fields + ('city','username', 'name', 'family_name', 'email', 'password1', 'password2', 'phone_number', 'address', 'is_buyer', 'is_seller')




#Form for changing password
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))  #using bootstrap to make sure all the forms look alike
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')