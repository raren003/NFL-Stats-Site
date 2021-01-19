from django.urls import path
from django.conf.urls import url
from rushers import views

app_name = 'rushers'
urlpatterns = [
    path('rusherspage/', views.rusher_page, name='rusher_page'),
]