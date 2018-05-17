from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from junk.models import Campus, Building, Floor


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ('id', 'name')


class BuildingSerializer(serializers.ModelSerializer):
    floors = serializers.StringRelatedField(many=True)
    # campus = CampusSerializer(read_only=True)
    included_serializers = {
        'campus': CampusSerializer
    }

    class Meta:
        model = Building
        fields = ('id', 'name', 'campus', 'floors')

    class JSONAPIMeta:
        included_resources = ['campus']


class BuildingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'name', 'campus')


class FloorSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(read_only=True)
    building_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Building.objects.all())
    included_serializers = {
        'building': BuildingSerializer
    }

    class Meta:
        model = Floor
        fields = ('id', 'building', 'name', 'building_id')

    class JSONAPIMeta:
        included_resources = ['building']
