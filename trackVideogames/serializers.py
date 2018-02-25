
from rest_framework.fields import CharField
from rest_framework.serializers import HyperlinkedModelSerializer
from models import Videogame


class VideogameSerializer(HyperlinkedModelSerializer):

    user = CharField(read_only=True)

    class Meta:
        model = Videogame
        fields = ('videogame_id','name', 'cover', 'user')