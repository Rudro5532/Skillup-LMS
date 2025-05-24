from django.contrib import admin
from .models import User

class AccountAdmin(admin.ModelAdmin):
    list_display = ("full_name", "username", "email", "subject", "is_teacher")
    list_display_links = ["full_name"]


admin.site.register(User,AccountAdmin)
