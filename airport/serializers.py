from rest_framework import serializers

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Order,
    Route,
    Crew,
    FlightCrewMember,
    Flight,
    Ticket,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer()

    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_row", "airplane_type")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    source = AirportSerializer()
    destination = AirportSerializer()

    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("route", "airplane", "departure_time", "arrival_time")


class FlightListSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    airplane = AirplaneSerializer()

    class Meta:
        model = Flight
        fields = ("route", "airplane", "departure_time", "arrival_time")


class FlightShortSerializer(serializers.ModelSerializer):
    airplane = AirplaneSerializer()

    class Meta:
        model = Flight
        fields = ("airplane", "departure_time", "arrival_time")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name")


class FlightCrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightCrewMember
        fields = ("flight", "crew")


class FlightCrewMemberListSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    crew = CrewSerializer()

    class Meta:
        model = FlightCrewMember
        fields = ("flight", "crew")


class FlightCrewMemberShortSerializer(serializers.ModelSerializer):
    crew = CrewSerializer()

    class Meta:
        model = FlightCrewMember
        fields = ("crew",)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("created_at",)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat", "flight", "order")


class TicketListSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    order = OrderSerializer()

    class Meta:
        model = Ticket
        fields = ("row", "seat", "flight", "order")
