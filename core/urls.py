from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sports/', views.sports_list, name='sports_list'),
    path('sports/<int:sport_id>/events/', views.event_list,  name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('buy-ticket/<int:ticket_type_id>/', views.buy_ticket,name='buy_ticket'),
]