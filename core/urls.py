from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sports/', views.sports_list, name='sports_list'),
    path('sports/<int:sport_id>/events/', views.event_list,  name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/buy/', views.checkout, name='checkout'),
    path("tickets/<uuid:ticket_code>/", views.ticket_detail, name="ticket_detail"), 
    path("my-tickets/", views.my_tickets, name="my_tickets"),
]