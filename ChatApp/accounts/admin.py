from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'id', 'username', 'date_joined', 'is_staff', 'is_verified', 'is_online')
    list_filter = ('is_staff', 'is_verified', 'is_online')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_verified', 'is_superuser', 'is_online')}),
        ('OTP', {'fields': ('otp',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_verified', 'is_superuser', 'is_online', 'otp'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('date_joined',)

admin.site.register(Account, AccountAdmin)




from django.contrib import admin
from .models import Account, UserInterest, FriendRequest


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'interest', 'preference_score')

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'accepted')

# Register your models and their respective admin classes here.
