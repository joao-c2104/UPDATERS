from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """Formulário para atualizar informações básicas do usuário"""
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'})
    )
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'})
    )
    last_name = forms.CharField(
        label="Sobrenome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        }
        labels = {
            'username': 'Nome de usuário',
        }


class ProfileUpdateForm(forms.ModelForm):
    """Formulário para atualizar informações do perfil"""
    profile_picture = forms.ImageField(
        label="Foto de Perfil",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    class Meta:
        model = Profile
        fields = ['profile_picture', 'font_size', 'preferred_categories']
        widgets = {
            'font_size': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'font_size': 'Tamanho da Fonte',
            'preferred_categories': 'Categorias Preferidas',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get categories from feed app
        from feed.models import Category
        categories = Category.objects.all()
        
        # Create checkbox choices
        category_choices = [(cat.id, cat.name) for cat in categories]
        self.fields['preferred_categories'] = forms.MultipleChoiceField(
            choices=category_choices,
            required=False,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            label='Categorias Preferidas'
        )
        
        # Set initial values from JSONField
        if self.instance and self.instance.preferred_categories:
            try:
                if isinstance(self.instance.preferred_categories, list):
                    # Convert list of IDs to integers if they're strings
                    initial_ids = [int(id) if isinstance(id, str) else id for id in self.instance.preferred_categories]
                else:
                    initial_ids = []
                self.fields['preferred_categories'].initial = initial_ids
            except (ValueError, TypeError):
                self.fields['preferred_categories'].initial = []


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulário personalizado para mudança de senha"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha atual'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nova senha'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar nova senha'})
        
        self.fields['old_password'].label = 'Senha Atual'
        self.fields['new_password1'].label = 'Nova Senha'
        self.fields['new_password2'].label = 'Confirmar Nova Senha'

