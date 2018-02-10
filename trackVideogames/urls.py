from django.conf.urls import url, include
from django.contrib import admin
from trackVideogames.models import Videogame
from django.views.generic import  ListView

urlpatterns = [
    url(r'$', ListView.as_view(
                    queryset=Videogame.objects.all(),
                    context_object_name='videogames',
                    template_name="index.html"), 
                    name='home'),
]
