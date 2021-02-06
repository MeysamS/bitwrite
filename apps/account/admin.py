from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_author',
    'special_user',
    'is_superuser',
    'groups',
    'user_permissions'
)

UserAdmin.list_display += ('is_author','is_special_user')
#    (None, {'fields': ('username', 'password')}),
