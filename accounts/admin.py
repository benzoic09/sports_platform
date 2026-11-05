from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count, Sum, Q

User = get_user_model()

paid = Q(ticket__status__in=["ACTIVE", "USED"])


class UserReportAdmin(UserAdmin):
    list_display = ("username", "email", "date_joined", "last_login",
                    "tickets_bought", "total_spent")

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