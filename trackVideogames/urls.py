from django.conf.urls import url
from trackVideogames.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^completed_video_games$', CompletedVideoGamesList.as_view(), name='completed-vg'),
    url(r'pendent_video_games$', PendentVideoGamesList.as_view(), name='pendent-vg'),
    url(r'^video_games/(?P<pk>\d+)/reviews/create/$',review, name='review_create'),
    url(r'^video_games/(?P<pk>\d+)/pendent/add/$', add_pendent, name='pendent_add'),
    url(r'^video_games/(?P<pk>\d+)/review/delete/$', delete_video_game_review, name='delete_review'),
]


# Nomes per l'autocomplete
urlpatterns += [
    # RESTful API
    url(r'^api/video_games/$',
        APIVideoGamesList.as_view(), name='video-games-list'),
]

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'xml'])