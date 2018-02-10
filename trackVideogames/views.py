# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from trackVideogames.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Security Mixins
class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CheckIsOwnerMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOwnerMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

class LoginRequiredCheckIsOwnerUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    template_name = 'form.html'


# Create your views here.
class HomePage(ListView):
    template_name = 'index.html'
    model = Videogame

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        all_videogames =  Videogame.objects.all()
        paginator = Paginator(all_videogames, 24)
        page = self.request.GET.get('page')
        
        try:
            vgs = paginator.page(page)
        except PageNotAnInteger:
            vgs = paginator.page(1)
        except EmptyPage:
            vgs = paginator.page(paginator.num_pages)

        context['videogames'] = vgs
        return context