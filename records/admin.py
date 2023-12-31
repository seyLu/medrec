from django.contrib import admin

from .models import Record, RecordUpdateHistory


class RecordUpdateHistoryInline(admin.TabularInline):  # type: ignore[type-arg]
    model = RecordUpdateHistory
    extra = 0


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin[Record]):
    list_display = ("client", "history", "diagnosis_and_plan", "remarks")
    inlines = [RecordUpdateHistoryInline]
