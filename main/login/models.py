from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


class Profile(models.Model):
    FONT_SIZE_CHOICES = [
        ('small', 'Pequeno'),
        ('medium', 'Médio'),
        ('large', 'Grande'),
        ('x-large', 'Extra Grande'),
    ]
    
    ACCOUNT_TIER_CHOICES = [
        ('free', 'Gratuito'),
        ('premium', 'Premium'),
        ('jcplus', 'JC Plus'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Foto de Perfil")
    font_size = models.CharField(
        max_length=10,
        choices=FONT_SIZE_CHOICES,
        default='medium',
        verbose_name="Tamanho da Fonte"
    )
    account_tier = models.CharField(
        max_length=10,
        choices=ACCOUNT_TIER_CHOICES,
        default='free',
        verbose_name="Tipo de Conta"
    )
    preferred_categories = models.JSONField(default=list, blank=True, verbose_name="Categorias Preferidas")
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()