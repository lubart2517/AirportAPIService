from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirplaneViewSet,
    AirportViewSet,
    AirplaneTypeViewSet,
    RouteViewSet,
    FlightViewSet,
    CrewViewSet,
    FlightCrewMemberViewSet,
    OrderViewSet,
    TicketViewSet
)


router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("crews", CrewViewSet)
router.register("flight_crew_members", FlightCrewMemberViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
