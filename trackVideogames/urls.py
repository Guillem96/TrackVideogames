from django.conf.urls import url, include
from django.contrib import admin
from trackVideogames.views import HomePage
from django.views.generic import  ListView

urlpatterns = [
    url(r'$', HomePage.as_view(), name='home'),
]
