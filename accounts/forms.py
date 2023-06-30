from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser



  
class SignUpForm(UserCreationForm): 
      
     class Meta(UserCreationForm):  
         model = CustomUser  
         fields = UserCreationForm.Meta.fields + ('city','username', 'name', 'family_name', 'email', 'password1', 'password2', 'phone_number', 'address', 'is_buyer', 'is_seller')


# class SignUpForm(UserCreationForm):
#     name = forms.CharField(max_length=100, required=True)
#     family_name = forms.CharField(max_length=100, required=True)
#     username = forms.CharField(max_length=50, required=True)
#     email = forms.EmailField(required=False)  #can be left blank
#     city = forms.CharField(max_length=50, required=True)
#     phone_number = forms.CharField(max_length=11, required=True)
#     address = forms.CharField(required=True)
#     is_buyer = forms.ChoiceField(choices=[('buyer', 'Ordinary Customer')], widget=forms.RadioSelect())
#     is_seller = forms.ChoiceField(choices=[('seller', 'Wholesale Customer')], widget=forms.RadioSelect())
#     # is_buyer = forms.BooleanField(required=False, initial=True)
#     # is_seller = forms.BooleanField(required=False, initial=False)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'name', 'family_name', 'email', 'city', 'password1', 'password2', 'phone_number', 'address', 'is_buyer', 'is_seller')

#Form for changing password
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))  #using bootstrap to make sure all the forms look alike
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')