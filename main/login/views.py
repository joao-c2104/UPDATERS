from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .forms import UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile

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


@login_required
def user_settings(request):
    """Página de configurações do usuário"""
    user = request.user
    
    # Garantir que o perfil existe
    profile, created = Profile.objects.get_or_create(user=user)
    
    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateForm(instance=profile)
    password_form = CustomPasswordChangeForm(user=user)
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'user_info':
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Informações do usuário atualizadas com sucesso!")
                return redirect('user_settings')
            else:
                messages.error(request, "Por favor, corrija os erros no formulário.")
        
        elif form_type == 'profile_info':
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                # Handle preferred_categories - convert to list of IDs (as integers)
                preferred_categories = profile_form.cleaned_data.get('preferred_categories', [])
                # Convert string IDs from form to integers for JSONField
                profile.preferred_categories = [int(cat_id) for cat_id in preferred_categories] if preferred_categories else []
                # Save the profile instance directly to ensure preferred_categories is saved
                profile.save()
                # Also save the form to handle other fields like profile_picture and font_size
                profile_form.save()
                messages.success(request, "Perfil atualizado com sucesso!")
                return redirect('user_settings')
            else:
                messages.error(request, "Por favor, corrija os erros no formulário.")
        
        elif form_type == 'password_change':
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Senha alterada com sucesso!")
                return redirect('user_settings')
            else:
                messages.error(request, "Por favor, corrija os erros no formulário.")
    
    # Re-initialize forms to get updated data
    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateForm(instance=profile)
    password_form = CustomPasswordChangeForm(user=user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': profile,
    }
    
    return render(request, 'login/settings.html', context)