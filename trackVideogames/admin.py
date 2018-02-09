# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Videogame, Genre, Theme, VideogameReview

# Register your models here.
admin.site.register(Videogame)
admin.site.register(Genre)
admin.site.register(Theme)
admin.site.register(VideogameReview)
