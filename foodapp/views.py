import json

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


def home(request):
    if request.user.is_authenticated:
        redirect("restaurants")
        return render(request, "restaurants.html")
    else:
        return render(request, "home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("/restaurants")
        else:
            messages.error(request, 'Username or password incorrect')
            return render(request, "login.html")
    else:
        return render(request, "login.html")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect("/")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username not available!')
            redirect("accounts/register")
            return render(request, "register.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already registered on this Email!')
            redirect("register")
            return render(request, "register.html")
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            redirect("accounts/login")
            messages.success(request, 'Registered Successfully! Login to continue')
            return render(request, "login.html")
    else:
        return render(request, "register.html")
