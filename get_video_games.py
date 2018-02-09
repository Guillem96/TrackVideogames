from igdb_api_python.igdb import igdb
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PracticaPrevia.settings")
django.setup()

from trackVideogames import models

igdb = igdb('b39ab80da1d9eac24dc7ae18954930c0')

def get_genres():
    result = igdb.genres({'limit':50})
    for genre in result.body:
        g = models.Genre(genre_id=genre["id"], name=genre["name"])
        g.save()


get_genres()