from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
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

    def purchase_tickets(self, user, quantity):

        if quantity < 1:
            raise ValueError("Please choose at least 1 ticket.")

        if quantity > 10:
            raise ValueError("You can buy a maximum of 10 tickets at a time.")

        with transaction.atomic():
            # Lock this row so two buyers can't take the last tickets together
            ticket_type = TicketType.objects.select_for_update().get(pk=self.pk)

            if ticket_type.event.event_date < timezone.localdate():
                raise ValueError("This event has already taken place.")

            if ticket_type.available_quantity == 0:
                raise ValueError("Sorry, these tickets are sold out.")

            if ticket_type.available_quantity < quantity:
                raise ValueError(f"Only {ticket_type.available_quantity} tickets left.")

            tickets = [
                Ticket.objects.create(user=user, ticket_type=ticket_type)
                for _ in range(quantity)
            ]

            ticket_type.available_quantity -= quantity
            ticket_type.save()

        return tickets

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