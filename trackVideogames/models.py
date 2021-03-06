# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __unicode__(self):
        return u"%s" % self.name


class Theme(models.Model):
    theme_id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __unicode__(self):
        return u"%s" % self.name


class Videogame(models.Model):
    videogame_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    summary = models.TextField()
    released = models.DateField(null=True)
    cover = models.ImageField(upload_to="trackVideogames")
    genres = models.ManyToManyField(Genre)
    user = models.ForeignKey(User, default=1)
    themes = models.ManyToManyField(Theme)

    def __unicode__(self):
        return u"%s" % self.name


class VideogameReview(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    user = models.ForeignKey(User, default=1)
    videogame = models.ForeignKey(Videogame, default=1)
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=RATING_CHOICES, null=True)
    date = models.DateField(null=True)
    comment = models.TextField(null=True)
    time_to_beat = models.IntegerField(null=True)
    completed = models.BooleanField()

    class Meta:
        unique_together = ("videogame", "user")