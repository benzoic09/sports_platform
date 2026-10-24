from django.contrib import admin
from .models import TicketType, Ticket

admin.site.register(TicketType)
admin.site.register(Ticket)