from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from junk.models import Building, Floor, Campus
from junk.serializers import BuildingSerializer, BuildingCreateSerializer, FloorSerializer


# class BuildingViewSet(viewsets.ModelViewSet):
#     queryset = Building.objects.all()
#     serializer_class = BuildingSerializer


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method in ('GET', ):
            return BuildingSerializer
        else:
            return BuildingCreateSerializer

    def find_or_create_related(self, request, clazz, item_name, required):
        obj = None

        # Try to find an embedded id in the request for an existing object
        obj_id = request.data.pop(item_name+"_id", None)
        if obj_id:
            obj = clazz.objects.filter(pk=obj_id).first()

        # Next, is an object embedded to have a new object created in this request
        if not obj:
            obj_info = request.data.pop(item_name, None)
            if obj_info:
                obj = clazz.objects.create(**obj_info)

        # Finally if nothing else, create a blank object
        if required and obj is None:
            obj = clazz.objects.create()

        return obj

    def create(self, request):
        #
        # #print("REQUEST -----------", request.META, "-----------", request.data, "----------")
        #
        # campus = None
        # campus_id = request.data.pop("campus_id", None)
        # print("%%%%%%%%%%%%%%%%%%%% ", campus_id, "^%%%%%%%%%%%%%%%")
        # if campus_id:
        #     print("GETTING CAMPUS FROM", campus_id)
        #     campus = Campus.objects.filter(pk=campus_id).first()
        #
        # if campus is None:
        #     campus_info = request.data.pop("campus", None)
        #     print("%%%%%%%%%%%%%%%%%%%% ", campus_info, "^%%%%%%%%%%%%%%%")
        #     if campus_info is not None:
        #         print("MAKING CAMPUS FROM", campus_info)
        #         campus = Campus.objects.create(**campus_info)
        #
        #
        # if campus is None:
        #     print("BRAND NEW CAMPUS")
        #     campus = Campus.objects.create()
        #
        campus = self.find_or_create_related(request, Campus, 'campus', True)
        request.data['name'] = str(request.data['name']).upper() + "GARBAGE"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("VALIDATES -----------", serializer.validated_data, "----------", serializer.is_valid, "----------")
        building = self.perform_create(serializer)
        building.campus = campus   # find_or_create_related(request, Campus, 'campus', True)
        building.save()
        # if campus is not None:
        #     building.campus = campus
        #     building.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)
