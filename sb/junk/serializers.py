from rest_framework import serializers
from junk.models import Campus, Building, Floor


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ('id', 'name')


class BuildingSerializer(serializers.ModelSerializer):
    floors = serializers.StringRelatedField(many=True)
    campus = CampusSerializer(read_only=True)

    class Meta:
        model = Building
        fields = ('id', 'name', 'campus', 'floors')


class BuildingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'name', 'campus')


class FloorSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(read_only=True)
    building_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Building.objects.all())

    class Meta:
        model = Floor
        fields = ('id', 'building', 'name', 'building_id')
