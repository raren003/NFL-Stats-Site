from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'standings'
urlpatterns = [
    path('standings/', views.standings, name='standings'),
]
