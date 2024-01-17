from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirplaneViewSet,
    AirportViewSet,
    AirplaneTypeViewSet,
    RouteViewSet,
    FlightViewSet
)


router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
