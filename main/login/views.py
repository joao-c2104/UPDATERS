from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def login_user(request: HttpRequest) -> HttpResponse:
    return render(request, 'login/login.html')

def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')

def submit_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        usuario = authenticate(username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido")
            return redirect('login_user') 
    else:
        return redirect('/')
        
def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('full_name')  
        email = request.POST.get('email')
        password = request.POST.get('password')


        if not username:
            username = email.split('@')[0] 
        

        if not User.objects.filter(username=username).exists():
            
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect('login_user')
        else:
            messages.error(request, "Nome de usuário já existe.")

    return render(request, 'login/register.html')


def forgot_password(request: HttpRequest) -> HttpResponse:
    return render(request, 'login/forgot_password.html')


def submit_forgot_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email_or_username = request.POST.get('email')
        
        user = None
        try:
            user = User.objects.get(email__iexact=email_or_username) 
        except User.DoesNotExist:
            try:
                user = User.objects.get(username__iexact=email_or_username)
            except User.DoesNotExist:
                pass
        
        messages.info(request, "Se a conta for encontrada, você receberá um link de redefinição por e-mail.")
        
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            pass 
            
        return redirect('login_user') 
    
    return redirect('forgot_password')