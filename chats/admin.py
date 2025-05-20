from django.contrib import admin
from .models import Chat


@admin.register(Chat)
class Admin(admin.ModelAdmin):
    list_display = ("id", "role", "content", "document", "created_at")
