from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "E-mail ou senha incorretos.")
    
    return render(request, 'login/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect('login_user')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está em uso.")
            return redirect('register_user')
        
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect('login_user')

    return render(request, 'login/register.html')

def forgot_password(request):
    return render(request, 'login/forgot_password.html')

def submit_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(f"LINK DE RECUPERAÇÃO (SIMULADO): /reset/{uid}/{token}/")
            
            messages.success(request, "Se este e-mail existir, um link de recuperação foi enviado.")
        except User.DoesNotExist:
            messages.success(request, "Se este e-mail existir, um link de recuperação foi enviado.")
            
        return redirect('login_user') 
    
    return redirect('forgot_password')