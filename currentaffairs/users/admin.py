from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'email',
        'first_name',
        'last_name',
        'native_language',
        'is_guest',
        'color_scheme',
        'has_avatar',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'native_language',
        'is_guest',
        'color_scheme',
        'is_staff',
        'is_active',
    )

    ordering = ('email',)

    search_fields = (
        'email',
        'first_name',
        'last_name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password'
            )
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'avatar',
                'native_language',
                'color_scheme',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_guest',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'native_language',
                'is_guest',
                'color_scheme',
            ),
        }),
    )

    def has_avatar(self, obj):
        return bool(obj.avatar)

    has_avatar.boolean = True
    has_avatar.short_description = 'Avatar'
