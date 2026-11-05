from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum

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
def checkout(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.event_date < timezone.localdate():
        messages.error(request, "This event has already taken place.")
        return redirect(f"/events/{event.id}/")

    ticket_types = event.ticket_types.filter(available_quantity__gt=0)
    selected = request.GET.get("ticket_type", "")   # preselected from the event page

    if request.method == "POST":
        selected = request.POST.get("ticket_type", "")

        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 0

        ticket_type = None
        if selected.isdigit():
            ticket_type = event.ticket_types.filter(id=selected).first()

        if ticket_type is None:
            messages.error(request, "Please choose a ticket type.")
        else:
            try:
                tickets = ticket_type.purchase_tickets(request.user, quantity)
            except ValueError as error:
                messages.error(request, str(error))
            else:
                count = len(tickets)
                messages.success(
                    request,
                    f"{count} ticket{'s' if count != 1 else ''} purchased successfully!"
                )
                return redirect("/my-tickets/")

    return render(request, "core/checkout.html", {
        "event": event,
        "ticket_types": ticket_types,
        "selected": selected,
    })


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
    query = request.GET.get("q", "").strip()

    tickets = (
        Ticket.objects
        .filter(user=request.user)
        .select_related("ticket_type__event")
        .order_by("-purchased_at")
    )

    if query:
        tickets = tickets.filter(
            Q(ticket_type__event__title__icontains=query)
            | Q(ticket_type__event__sport__name__icontains=query)
            | Q(ticket_type__name__icontains=query)
        )

    total_spent = (
        tickets.exclude(status="CANCELLED")
        .aggregate(total=Sum("ticket_type__price"))["total"] or 0
    )

    return render(request, "core/my_tickets.html", {
        "tickets": tickets,
        "today": timezone.localdate(),
        "query": query,
        "total_spent": total_spent,
    })