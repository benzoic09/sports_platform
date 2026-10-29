from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.decorators import login_required
from ticketing.models import TicketType
from sports.models import Sport
from events.models import Event

def home(request):
    events = Event.objects.all()[:4]

    return render(request, "core/home.html", {"events": events})


def sports_list(request):
    sports = Sport.objects.all()

    return render(
        request,
        'core/sports_list.html',
        {'sports': sports}
    )

def event_list(request, sport_id):

    events = Event.objects.filter(
        sport_id=sport_id
    )

    return render(
        request,
        'core/event_list.html',
        {'events': events}
    )

def event_detail(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    return render(
        request,
        'core/event_detail.html',
        {'event': event}
    )

@login_required
def buy_ticket(request, ticket_type_id):

    ticket_type = get_object_or_404(
        TicketType,
        id=ticket_type_id
    )

    ticket = ticket_type.purchase_ticket(
        request.user
    )

    return render(
        request,
        'core/ticket_success.html',
        {'ticket': ticket}
    )