from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Benutzer-Modell erweitern
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')  # Zeigt wichtige Felder in der Liste an
    list_filter = ('is_staff', 'is_active', 'is_superuser')  # Filter nach Status
    search_fields = ('username', 'email')  # Ermöglicht die Suche nach Benutzernamen und E-Mail
    ordering = ('username',)  # Sortiert Benutzer alphabetisch
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

# Standard-Benutzer-Modell registrieren
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
