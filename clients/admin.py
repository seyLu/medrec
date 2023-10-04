from django.contrib import admin

from .models import Client


@admin.register(Client)
class UserAdmin(admin.ModelAdmin[Client]):
    pass
