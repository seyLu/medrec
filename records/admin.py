from typing import Any

from django.contrib import admin
from django.forms import Form
from django.http import HttpRequest

from .models import Record, RecordUpdateHistory


class RecordUpdateHistoryInline(admin.TabularInline):
    model = RecordUpdateHistory
    extra = 0


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin[Record]):
    list_display = ("client", "history", "diagnosis_and_plan", "remarks")
    inlines = [RecordUpdateHistoryInline]

    @admin.display(description="client")
    def client(self, obj: Record) -> str:
        return obj.client_reference_number

    def save_model(
        self, request: HttpRequest, obj: Record, form: Form, change: Any
    ) -> None:
        if obj is None:
            obj.save()

        record_update_history = RecordUpdateHistory(
            record=obj,
            updated_by=request.user,
            remarks=obj.remarks,
        )
        record_update_history.save()
        super().save_model(request, obj, form, change)
