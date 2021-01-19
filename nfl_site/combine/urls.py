from django.urls import path
from django.conf.urls import url
from combine import views

app_name = 'combine'
urlpatterns = [
    path('combinepage/', views.combine_page, name='combine_page'),
]