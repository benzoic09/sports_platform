from django.urls import path
from .views import register, UserLoginView, user_logout

urlpatterns = [
    path('register/', register, name='register'),

    path('login/', UserLoginView.as_view(),name='login'),

    path(
        'logout/', user_logout, name='logout'),
]