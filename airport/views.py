import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Order,
    Route,
    Crew,
    FlightCrewMember,
    Flight,
    Ticket
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
#from airport.tasks import post_create_delay

from airport.serializers import (
    AirportSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    RouteSerializer,
    FlightSerializer,
    CrewSerializer,
    FlightCrewMemberSerializer,
    OrderSerializer,
    TicketSerializer
)


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airport.objects
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        """Retrieve the airports with filters"""
        name = self.request.query_params.get("name")
        city = self.request.query_params.get("city")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        if city:
            queryset = queryset.filter(closest_big_city__icontains=city)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by airport name (ex. ?name=Orly)",
            ),
            OpenApiParameter(
                "city",
                type=OpenApiTypes.STR,
                description="Filter by airport closest city (ex. ?closest_big_city=Newbie)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirplaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airplane.objects
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        """Retrieve the airplanes with filters"""
        name = self.request.query_params.get("name")
        airplane_type = self.request.query_params.get("airplane_type")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        if airplane_type:
            queryset = queryset.filter(airplane_type__icontains=airplane_type)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by airplane name (ex. ?name=A380)",
            ),
            OpenApiParameter(
                "airplane_type",
                type=OpenApiTypes.STR,
                description="Filter by airplane type (ex. ?airplane_type=Airbus)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AirplaneType.objects
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Route.objects
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        """Retrieve the routes with filters"""
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(source__icontains=source)

        if destination:
            queryset = queryset.filter(destination__icontains=destination)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by route source (ex. ?source=Orly)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filter by route destination (ex. ?destination=Orly)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Flight.objects
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        """Retrieve the flights with filters"""
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        date_format = "%Y-%m-%d"

        departure_day = self.request.query_params.get("departure_day")
        arrival_day = self.request.query_params.get("arrival_day")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(route__source__name__icontains=source)

        if destination:
            queryset = queryset.filter(route__destination__name__icontains=destination)

        if departure_day:
            day = datetime.datetime.strptime(departure_day, date_format)
            queryset = queryset.filter(departure_time__date=day)

        if arrival_day:
            day = datetime.datetime.strptime(arrival_day, date_format)
            queryset = queryset.filter(arrival_time__date=day)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by flight route source (ex. ?source=Orly)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filter by flight route destination (ex. ?destination=Orly)",
            ),
            OpenApiParameter(
                "departure_day",
                type=OpenApiTypes.STR,
                description="Filter by flight departure day (ex. ?departure_time.day=2024-01-22)",
            ),
            OpenApiParameter(
                "arrival_day",
                type=OpenApiTypes.STR,
                description="Filter by flight arrival day (ex. ?arrival_time.day=2024-01-22)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)