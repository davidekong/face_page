from . import views
from django.urls import path

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('room/<pk>', views.room, name='room')
]
