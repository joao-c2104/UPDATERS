# Generated manually for Profile model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Foto de Perfil')),
                ('font_size', models.CharField(choices=[('small', 'Pequeno'), ('medium', 'Médio'), ('large', 'Grande'), ('x-large', 'Extra Grande')], default='medium', max_length=10, verbose_name='Tamanho da Fonte')),
                ('account_tier', models.CharField(choices=[('free', 'Gratuito'), ('premium', 'Premium'), ('jcplus', 'JC Plus')], default='free', max_length=10, verbose_name='Tipo de Conta')),
                ('preferred_categories', models.JSONField(blank=True, default=list, verbose_name='Categorias Preferidas')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfis',
            },
        ),
    ]

