from rest_framework import serializers

from game.models import *


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'
