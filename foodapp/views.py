from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            return redirect("/")
        else:
            messages.error(request, 'Username or password incorrect')
            return render(request, "login.html")
    else:
        return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username not available!')
            redirect("register")
            return render(request, "register.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already registered on this Email!')
            redirect("register")
            return render(request, "register.html")
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            redirect("login")
            messages.success(request, 'Registered Successfully! Login to continue')
            return render(request, "login.html")
    else:
        return render(request, "register.html")
