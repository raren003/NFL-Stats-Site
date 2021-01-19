from django.urls import path
from django.conf.urls import url
from player_management import views

app_name = 'player_management'
urlpatterns = [
    path('PlayerManagement/', views.player_management, name='player_management'),
]