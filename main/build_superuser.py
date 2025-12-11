import os
import django
from django.contrib.auth import get_user_model

# Configura o ambiente do Django para o script funcionar
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

User = get_user_model()

# Pega os dados das variáveis de ambiente (ou usa padrão se não encontrar)
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin_render')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@render.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'senha12345')

def create_superuser():
    if User.objects.filter(username=username).exists():
        print(f"Superusuário '{username}' já existe. Nada a fazer.")
    else:
        print(f"Criando superusuário '{username}'...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superusuário criado com sucesso!")

if __name__ == "__main__":
    create_superuser()