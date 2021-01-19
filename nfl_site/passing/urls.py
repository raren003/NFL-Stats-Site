from django.urls import path
from django.conf.urls import url
from passing import views

app_name = 'passing'
urlpatterns = [
    path('passerpage/', views.pass_page, name='pass_page'),
]