from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST

from ticketing.models import TicketType, Ticket
from sports.models import Sport
from events.models import Event
from .utils import make_qr


def home(request):
    today = timezone.localdate()
    events = Event.objects.filter(event_date__gte=today).order_by("event_date")[:4]

    return render(request, "core/home.html", {"events": events})


def sports_list(request):
    sports = Sport.objects.filter(is_active=True)

    return render(
        request,
        'core/sports_list.html',
        {'sports': sports}
    )


def event_list(request, sport_id):
    sport = get_object_or_404(Sport, id=sport_id)
    today = timezone.localdate()

    upcoming = Event.objects.filter(
        sport_id=sport_id, event_date__gte=today
    ).order_by("event_date")

    past = Event.objects.filter(
        sport_id=sport_id, event_date__lt=today
    ).order_by("-event_date")

    return render(request, 'core/event_list.html', {
        'sport': sport,
        'upcoming': upcoming,
        'past': past,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_past = event.event_date < timezone.localdate()

    return render(request, 'core/event_detail.html', {
        'event': event,
        'is_past': is_past,
    })


@login_required
@require_POST
def buy_ticket(request, ticket_type_id):
    ticket_type = get_object_or_404(TicketType, id=ticket_type_id)

    try:
        ticket = ticket_type.purchase_ticket(request.user)
    except ValueError as error:
        messages.error(request, str(error))
        return redirect(f"/events/{ticket_type.event.id}/")

    messages.success(request, "Ticket purchased successfully!")
    return redirect(f"/tickets/{ticket.ticket_code}/")


@login_required
def ticket_detail(request, ticket_code):
    # user=request.user means nobody can open someone else's ticket
    ticket = get_object_or_404(Ticket, ticket_code=ticket_code, user=request.user)
    qr_code = make_qr(str(ticket.ticket_code))

    return render(request, "core/ticket_detail.html", {
        "ticket": ticket,
        "qr_code": qr_code,
    })


@login_required
def my_tickets(request):
    tickets = (
        Ticket.objects
        .filter(user=request.user)
        .select_related("ticket_type__event")
        .order_by("-purchased_at")
    )

    return render(request, "core/my_tickets.html", {
        "tickets": tickets,
        "today": timezone.localdate(),
    })