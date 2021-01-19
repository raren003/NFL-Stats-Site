"""nfl_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from response import views as resp_views
from combine import views as combine_views
from standings import views as standings_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('response/', include('response.urls')),
    #default url goes straight to response
    path('',include('response.urls')),
    # URL path for combine app
    path('',include('combine.urls')),
    path('',include('passing.urls')),
    path('',include('rushers.urls')),
    path('', include('receiving.urls')),
    path('', include('player_management.urls')),
    path('', include('standings.urls')),
]
