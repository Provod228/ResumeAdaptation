from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('username', 'email', 'nickname', 'email_verified', 'is_staff', 'provider')

    # Поля, по которым можно кликнуть для перехода к редактированию
    list_display_links = ('username', 'email')

    # Боковая панель фильтрации
    list_filter = ('is_staff', 'email_verified', 'provider', 'is_active')

    # Поля для быстрого поиска
    search_fields = ('username', 'email', 'nickname', 'social_id')

    # Автоматическая генерация slug при редактировании в админке
    prepopulated_fields = {'slug': ('username',)}

    # Группировка полей внутри самой формы редактирования пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('nickname', 'avatar', 'slug', 'email_verified')
        }),
        ('Социальные сети (OAuth2)', {
            'fields': ('social_avatar', 'social_id', 'provider'),
            'classes': ('collapse',),  # Сворачиваемая группа полей
        }),
    )

    # Группировка полей при создании нового пользователя через админку
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {
            'fields': ('email', 'nickname', 'slug'),
        }),
    )