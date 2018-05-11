from rest_framework import serializers
from .models import *


class BuildingSerializer(serializers.ModelSerializer):
    floors = serializers.StringRelatedField(many=True)
    # floors = serializers.PrimaryKeyRelatedField(many=True)  # does not work

    class Meta:
        model = Building
        fields = ('id', 'name', 'floors')


class FloorSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(read_only=True)

    class Meta:
        model = Floor
        fields = ('id', 'building', 'name')
