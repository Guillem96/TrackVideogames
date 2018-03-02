# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context_processors import csrf
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import permissions, generics
from rest_framework.response import Response

from serializers import VideogameSerializer
from trackVideogames.models import *
from datetime import datetime


# Security Mixins
class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


# Funció per paginar una llsita d'objectes en una ListView
def pagination(objects, page, items_per_page=24):
    paginator = Paginator(objects, items_per_page)

    try:
        obj_paginated = paginator.page(page)
    except PageNotAnInteger:
        obj_paginated = paginator.page(1)
    except EmptyPage:
        obj_paginated = paginator.page(paginator.num_pages)

    return obj_paginated


# Create your views here.
class HomePage(ListView):
    template_name = 'index.html'
    model = Videogame

    def get_context_data(self, **kwargs):
        video_games = Videogame.objects.order_by('name')
        genres = []
        themes = []

        # Obtenir la query que s'ha realitzat
        path = self.request.get_full_path()
        query = path.split("?")[1] if '?' in path else ""
        query = re.sub(r'page=[0-9]+&*', "", query) # Eliminar la pagina de la query

        # Obtenir valors de la cerca
        for key in self.request.GET:
            if key == 'name':
                if self.request.GET['name'] != "":
                    video_games = video_games.filter(name__contains=self.request.GET['name'])
            else:
                if key.startswith("t_"):
                    themes.append(int(key.split("_")[1]))
                elif key.startswith("g_"):
                    genres.append(int(key.split("_")[1]))

        # Filtrar els videojocs
        if genres:
            video_games = video_games.filter(genres__genre_id__in=genres)

        if themes:
            video_games = video_games.filter(themes__theme_id__in=themes)

        # Establir context per a la template
        context = super(ListView, self).get_context_data(**kwargs)
        context['themes'] = Theme.objects.order_by('name')
        context['genres'] = Genre.objects.order_by('name')
        context['query'] = query
        context['videogames'] = pagination(video_games, self.request.GET.get('page'))
        return context


class CompletedVideoGamesList(LoginRequiredMixin, ListView):
    template_name = 'completed_video_games.html'
    model = VideogameReview

    def get_context_data(self, **kwargs):
        video_games = VideogameReview.objects.filter(user=self.request.user, completed=True).order_by("videogame__name")

        # Establir context per a la template
        context = super(ListView, self).get_context_data(**kwargs)
        context['videogames'] = video_games

        return context


class PendentVideoGamesList(LoginRequiredMixin, ListView):
    template_name = 'pendent_video_games.html'
    model = VideogameReview

    def get_context_data(self, **kwargs):
        video_games = VideogameReview.objects.filter(user=self.request.user, completed=False).order_by("videogame__name")

        # Establir context per a la template
        context = super(ListView, self).get_context_data(**kwargs)
        context['videogames'] = video_games

        return context


@login_required()
def review(request, pk):
    video_game = get_object_or_404(Videogame, pk=pk)
    if VideogameReview.objects.filter(videogame=video_game, user=request.user).exists():
        VideogameReview.objects.get(videogame=video_game, user=request.user).delete()

    # Obtenir hores i minuts dedicats per posteriorment convertir-ho tot a minuts
    hours = int(request.POST['time-to-beat'].split("h ")[0])
    minutes = int(request.POST['time-to-beat'].split("h ")[1][:-3])

    VideogameReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        time_to_beat=hours * 60 + minutes,  # Expressat en minuts
        videogame=video_game,
        completed=True).save()
    return HttpResponseRedirect(reverse('trackVideogames:completed-vg'))


@login_required()
def add_pendent(request, pk):
    video_game = get_object_or_404(Videogame, pk=pk)
    if VideogameReview.objects.filter(videogame=video_game, user=request.user).exists():
        VideogameReview.objects.get(videogame=video_game, user=request.user).delete()

    date = datetime.strptime(request.POST['data-pendent'], '%Y-%m-%d')

    VideogameReview(
        user=request.user,
        videogame=video_game,
        completed=False,
        date=date).save()

    return HttpResponseRedirect(reverse('trackVideogames:pendent-vg'))


@login_required()
def delete_video_game_review(request, pk):
    video_game = get_object_or_404(VideogameReview, pk=pk)

    if not video_game.user == request.user:
        raise PermissionDenied

    video_game.delete()

    return HttpResponseRedirect(request.GET.get("next", "/trackVideogames"))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register/complete')

    else:
        form = UserCreationForm()
        token = {}
        token.update(csrf(request))
        token['form'] = form

    return render_to_response('../templates/registration/signup.html', token)

# API REST Nomes per a l'autocomplete
class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class APIVideoGamesList(IsOwnerOrReadOnly, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    model = Videogame
    queryset = Videogame.objects.all()
    serializer_class = VideogameSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.get('q'):
            queryset = Videogame.objects.filter(name__startswith=request.GET.get('q'))
        else:
            queryset = Videogame.objects.all()

        serializer = VideogameSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)

