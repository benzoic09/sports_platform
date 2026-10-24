from django.db import models
from django.conf import settings
from events.models import Event
import uuid


class TicketType(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='ticket_types'
    )

    name = models.CharField(max_length=50)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    available_quantity = models.PositiveIntegerField()

    def purchase_ticket(self, user):

        if self.available_quantity <= 0:
            raise ValueError("Tickets sold out")

        ticket = Ticket.objects.create(
            user=user,
            ticket_type=self
        )

        self.available_quantity -= 1
        self.save()

        return ticket

    def __str__(self):
        return f"{self.event.title} - {self.name}"

class Ticket(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE
    )

    ticket_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    purchased_at = models.DateTimeField(
        auto_now_add=True
    )

    is_used = models.BooleanField(
        default=False
    )
    STATUS_CHOICES = [
    ('ACTIVE', 'Active'),
    ('USED', 'Used'),
    ('CANCELLED', 'Cancelled'),
]

    status = models.CharField(
    max_length=10,
    choices=STATUS_CHOICES,
    default='ACTIVE'
)

    def __str__(self):
        return str(self.ticket_code)