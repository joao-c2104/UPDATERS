from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home') 
            return redirect(next_url)
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, 'login/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect('login_user')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "As senhas não coincidem.")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return redirect('register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está cadastrado.")
            return redirect('register_user')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect('login_user')

    return render(request, 'login/register.html')