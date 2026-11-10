import csv
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Sum, Q
from django.http import HttpResponse

User = get_user_model()

paid = Q(ticket__status__in=["ACTIVE", "USED"])


@admin.action(description="Export selected users to CSV")
def export_users_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="users_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Username", "Email", "Date joined", "Last login",
                     "Tickets bought", "Total spent (KES)"])

    for u in queryset:
        writer.writerow([
            u.username,
            u.email,
            u.date_joined.strftime("%Y-%m-%d"),
            u.last_login.strftime("%Y-%m-%d %H:%M") if u.last_login else "",
            u._tickets,
            u._spent or 0,
        ])

    return response


class UserReportAdmin(UserAdmin):
    list_display = ("username", "email", "date_joined", "last_login",
                    "tickets_bought", "total_spent")
    actions = [export_users_csv]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _tickets=Count("ticket", filter=paid),
            _spent=Sum("ticket__ticket_type__price", filter=paid),
        )

    @admin.display(ordering="_tickets", description="Tickets bought")
    def tickets_bought(self, obj):
        return obj._tickets

    @admin.display(ordering="_spent", description="Total spent (KES)")
    def total_spent(self, obj):
        return obj._spent or 0


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserReportAdmin)