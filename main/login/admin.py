from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_tier', 'font_size', 'get_preferred_categories_display')
    list_filter = ('account_tier', 'font_size')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações do Perfil', {
            'fields': ('profile_picture', 'font_size', 'account_tier', 'preferred_categories')
        }),
    )
    
    def get_preferred_categories_display(self, obj):
        if obj.preferred_categories:
            from feed.models import Category
            try:
                category_ids = [int(cat_id) if isinstance(cat_id, str) else cat_id for cat_id in obj.preferred_categories]
                categories = Category.objects.filter(id__in=category_ids)
                return ', '.join([cat.name for cat in categories])
            except (ValueError, TypeError):
                return 'N/A'
        return 'Nenhuma'
    get_preferred_categories_display.short_description = 'Categorias Preferidas'