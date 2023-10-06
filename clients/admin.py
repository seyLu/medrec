from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin[Client]):
    list_display = ("reference_number", "name", "type")

    @admin.display(description="name")
    def name(self, obj: Client):
        return obj.full_name
