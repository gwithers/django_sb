from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from junk import views

ROUTER = DefaultRouter(trailing_slash=False)
ROUTER.register(r'campus', views.CampusViewSet)
ROUTER.register(r'buildings', views.BuildingViewSet)
ROUTER.register(r'floors', views.FloorViewSet)

urlpatterns = [
    url(r'^', include(ROUTER.urls))
]
