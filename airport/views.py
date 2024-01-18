import datetime

from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
from airport.permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    IsOwner,
    IsAllowedToCreateOrAdmin
)


from airport.serializers import (
    AirportSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    RouteSerializer,
    FlightSerializer,
    FlightShortSerializer,
    CrewSerializer,
    FlightCrewMemberSerializer,
    FlightCrewMemberShortSerializer,
    OrderSerializer,
    TicketSerializer
)


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
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

    @action(
        methods=["GET"],
        detail=True,
        url_path="arrivals",
        permission_classes=[IsAuthenticated],
    )
    def arrivals(self, request, pk=None):
        """Endpoint to view airport routes"""
        arrivals = Route.objects.filter(
            destination=self.get_object()
        ).select_related("source", "destination")
        serializer = RouteSerializer(arrivals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="departures",
        permission_classes=[IsAuthenticated],
    )
    def departures(self, request, pk=None):
        """Endpoint to view airport routes"""
        arrivals = Route.objects.filter(
            source=self.get_object()
        ).select_related("source", "destination")
        serializer = RouteSerializer(arrivals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
                description=("Filter by airport closest city "
                             "(ex. ?closest_big_city=Newbie)"),
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
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airplane.objects.select_related("airplane_type")
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
            queryset = queryset.filter(
                airplane_type__icontains=airplane_type
            )

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
                description=("Filter by airplane type "
                             "(ex. ?airplane_type=Airbus)"),
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
    mixins.DestroyModelMixin,
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
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Route.objects.select_related("source", "destination")
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
                description=("Filter by route destination "
                             "(ex. ?destination=Orly)"),
            ),
        ]
    )
    @action(
        methods=["GET"],
        detail=True,
        url_path="flights",
        permission_classes=[IsAuthenticated],
    )
    def flights(self, request, pk=None):
        """Endpoint to view route flights"""
        flights = Flight.objects.filter(
            route=self.get_object()
        ).select_related(
            "airplane",
            "airplane__airplane_type"
        )
        serializer = FlightShortSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Flight.objects.select_related(
        "route",
        "route__source",
        "route__destination",
        "airplane",
        "airplane__airplane_type"
    )
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
            queryset = queryset.filter(
                route__destination__name__icontains=destination
            )

        if departure_day:
            day = datetime.datetime.strptime(departure_day, date_format)
            queryset = queryset.filter(departure_time__date=day)

        if arrival_day:
            day = datetime.datetime.strptime(arrival_day, date_format)
            queryset = queryset.filter(arrival_time__date=day)

        return queryset.distinct()

    @action(
        methods=["GET"],
        detail=True,
        url_path="crew_members",
        permission_classes=[IsAdminUser],
    )
    def crew_members(self, request, pk=None):
        """Endpoint to view flight crew members"""
        crew_members = FlightCrewMember.objects.filter(
            flight=self.get_object()
        ).select_related(
            "crew"
        )
        serializer = FlightCrewMemberShortSerializer(crew_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
                description=("Filter by flight route destination "
                             "(ex. ?destination=Orly)"),
            ),
            OpenApiParameter(
                "departure_day",
                type=OpenApiTypes.STR,
                description=("Filter by flight departure day "
                             "(ex. ?departure_time.day=2024-01-22)"),
            ),
            OpenApiParameter(
                "arrival_day",
                type=OpenApiTypes.STR,
                description=("Filter by flight arrival day "
                             "(ex. ?arrival_time.day=2024-01-22)"),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Crew.objects
    serializer_class = CrewSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        """Retrieve the crew with filters"""
        contains = self.request.query_params.get("contains")

        queryset = self.queryset

        if contains:
            queryset = queryset.filter(Q(
                first_name__icontains=contains
            ) | Q(
                last_name__icontains=contains
            ))

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "contains",
                type=OpenApiTypes.STR,
                description=("Filter by crew first_name or last_name"
                             "(ex. ?first_name=John or last_name=John)"),
            )

        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightCrewMemberViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FlightCrewMember.objects.select_related(
        "flight",
        "flight__route__source",
        "flight__route__destination",
        "flight__airplane",
        "flight__airplane__airplane_type",
        "crew"
    )
    serializer_class = FlightCrewMemberSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        """Retrieve the flight crew members with filters"""
        contains = self.request.query_params.get("contains")

        queryset = self.queryset

        if contains:
            queryset = queryset.filter(Q(
                crew__first_name__icontains=contains
            ) | Q(
                crew__last_name__icontains=contains
            ))

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "contains",
                type=OpenApiTypes.STR,
                description=("Filter by flight crew member "
                             "first_name or last_name"
                             "(ex. ?crew.first_name=John "
                             "or crew.last_name=John)"),
            )

        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects
    serializer_class = OrderSerializer
    permission_classes = (IsOwner, IsAdminUser)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ticket.objects.select_related(
        "order",
        "flight",
        "flight__route__source",
        "flight__route__destination",
        "flight__airplane",
        "flight__airplane__airplane_type",
    )
    serializer_class = TicketSerializer
    permission_classes = (IsAllowedToCreateOrAdmin,)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
