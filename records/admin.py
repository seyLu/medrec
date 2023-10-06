from django.contrib import admin

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
