# from django.contrib import admin
# from .models import User
# # Register your models here.


# admin.site.register(User)

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

User = get_user_model()

# Check if the model is already registered and unregister it
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Ignore if the User model is not already registered

# Register your custom User model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address')}),
    )

# Register other models
admin.site.register(Menu)
admin.site.register(LoginAttempt)
admin.site.register(Order)