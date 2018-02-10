from igdb_api_python.igdb import igdb
import os
from datetime import datetime
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
import urlparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PracticaPrevia.settings")
django.setup()

from trackVideogames import models

igdb = igdb('b39ab80da1d9eac24dc7ae18954930c0')

def save_image_from_url(field, url, image_name):
    if "https" not in url:
        r = requests.get("http:" + url)
    else:
        r = requests.get(url)

    if r.status_code == requests.codes.ok:

        img_temp = NamedTemporaryFile(delete = True)
        img_temp.write(r.content)
        img_temp.flush()

        field.save(image_name + "." + url.split(".")[-1], File(img_temp), save = True)

        return True

    return False


def get_genres():
    result = igdb.genres({'limit':50})
    for genre in result.body:
        g = models.Genre(genre_id=genre["id"], name=genre["name"])
        g.save()


def get_themes():
    result = igdb.themes({'limit':50})
    for theme in result.body:
        t = models.Theme(theme_id=theme["id"], name=theme["name"])
        t.save()

def get_video_games():
    offset = 0
    counter = 10
    models.Videogame.objects.all().delete()

    while counter > 0: 
        result = igdb.games({
                    'fields': 'id,name,popularity,themes,genres,first_release_date,cover,summary',
                    'order': 'popularity:desc',
                    'offset': offset,
                    'limit':50
                    })
        for game in result.body:
            g = models.Videogame(videogame_id=game["id"], name=game["name"])

            if "first_release_date" in game:
                g.released = datetime.fromtimestamp(game["first_release_date"]/1000)

            if "summary" in game:
                 g.summary = game["summary"]

            if "cover" in game:
                save_image_from_url( g.cover, game["cover"]["url"], str(g.videogame_id))
            
            g.save()
            if "themes" in game:
                for t in game["themes"]:
                    g.themes.add(models.Theme.objects.get(theme_id=t))

            if "genres" in game:
                for gen in game["genres"]:
                    g.genre.add(models.Genre.objects.get(genre_id=gen))
                    
        counter -= 1
        offset += 50

get_genres()
get_themes()
get_video_games()