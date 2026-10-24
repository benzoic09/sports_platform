from django.shortcuts import render

def home(request):
    return render(request, "core/home.html")


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