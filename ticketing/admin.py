import csv
from django.contrib import admin
from django.http import HttpResponse

from .models import TicketType, Ticket


@admin.action(description="Export selected tickets to CSV")
def export_tickets_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tickets_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Ticket code", "User", "Event", "Ticket type",
                     "Price (KES)", "Purchased", "Status"])

    for t in queryset.select_related("user", "ticket_type__event"):
        writer.writerow([
            t.ticket_code,
            t.user.username,
            t.ticket_type.event.title,
            t.ticket_type.name,
            t.ticket_type.price,
            t.purchased_at.strftime("%Y-%m-%d %H:%M"),
            t.status,
        ])

    return response


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("event", "name", "price", "quantity", "available_quantity")
    list_filter = ("event",)
    search_fields = ("name", "event__title")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_code", "user", "event", "ticket_type", "price", "purchased_at", "status")
    list_filter = ("status", "ticket_type__event", "purchased_at")
    search_fields = ("user__username", "user__email", "ticket_type__event__title")
    date_hierarchy = "purchased_at"
    actions = [export_tickets_csv]

    def event(self, obj):
        return obj.ticket_type.event

    def price(self, obj):
        return obj.ticket_type.price