from django.urls import path
from django.conf.urls import url
from receiving import views

app_name = 'receiving'
urlpatterns = [
    path('receivingpage/', views.receiving_page, name='receiving_page'),
    path('receivingpage/topreceivingpage/', views.top_receiving_page, name='top_receiving_page'),
    path('receivingpage/addreceiverpage/', views.add_receiver_page, name='add_receiver_page')
]
