from django.urls import path
from django.conf.urls import url
from response import views

app_name = 'response'
urlpatterns = [
    path('', views.home, name='home'),
    #path('rusherpage/',  views.rusher_page,  name='rusher_page'),
    #path('passerpage/',views.passer_page,name='passer_page'),
    # path('catcherpage/',views.catcher_page,name='catcher_page'),
    # Adding URL for combine page
    #path('combinepage/', views.combine_page,name='combine_page'),
]