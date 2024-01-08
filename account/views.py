from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
# Create your views here.


def creat_user(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
    else:
        messages.error(request, 'An error occurred during registration')
    return render(request, 'account/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('account:login')
