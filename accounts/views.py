from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, CustomPasswordChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

#LOGIN VIEW
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})

# #LOGOUT VIEW
# def logout_view(request):
#     logout(request)
#     return redirect('home')


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        print('form_valid called')
        return super().form_valid(form)

#SIGN UP VIEW
# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # log the user in
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})


#CHANGE THE PASSWORD VIEW
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # This makes sure that the user isn't logged out after changing password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

#def signup_view(request):
   # if request.method == 'POST':
   #     form = SignUpForm(request.POST)
    #    if form.is_valid():
    #        user = form.save()
    #        user.refresh_from_db()  # load the profile instance created by the signal
    #        user.is_buyer = form.cleaned_data.get('is_buyer')
    #        user.is_seller = form.cleaned_data.get('is_seller')
    #        user.save()
    #        raw_password = form.cleaned_data.get('password1')
    #        user = authenticate(username=user.username, password=raw_password)
    #        login(request, user)  #login the user and redirect to the home page
    #        return redirect('home')
    #else:
    #    form = SignUpForm()
    #return render(request, 'registration/signup.html', {'form': form})
