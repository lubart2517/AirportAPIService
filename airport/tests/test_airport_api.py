import datetime
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

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
from airport.serializers import (
    AirportSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    RouteSerializer,
    RouteListSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightShortSerializer,
    CrewSerializer,
    FlightCrewMemberSerializer,
    FlightCrewMemberShortSerializer,
    OrderSerializer,
    TicketSerializer,
)

AIRPORT_URL = reverse("airport:airport-list")
ROUTE_URL = reverse("airport:route-list")
AIRPLANETYPE_URL = reverse("airport:airplanetype-list")
FLIGHT_URL = reverse("airport:flight-list")
AIRPLANE_URL = reverse("airport:airplane-list")
CREW_URL = reverse("airport:crew-list")
FLIGHT_CREW_MEMBER_URL = reverse("airport:flightcrewmember-list")
ORDER_URL = reverse("airport:order-list")


def sample_airport(**params):
    defaults = {
        "name": "Sample airport",
        "closest_big_city": "Sample city",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def airport_detail_url(airport_id):
    return reverse("airport:airport-detail", args=[airport_id])


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        sample_airport()
        sample_airport()

        res = self.client.get(AIRPORT_URL)

        airports = Airport.objects.order_by("id")
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_airports_by_city(self):
        airport1 = sample_airport(closest_big_city="Paris")
        airport2 = sample_airport(closest_big_city="London")
        airport3 = sample_airport(closest_big_city="Lion")

        res = self.client.get(AIRPORT_URL, {"city": "on"})

        serializer1 = AirportSerializer(airport1)
        serializer2 = AirportSerializer(airport2)
        serializer3 = AirportSerializer(airport3)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)

    def test_retrieve_airport_detail(self):
        airport = sample_airport()
        url = airport_detail_url(airport.id)
        res = self.client.get(url)

        serializer = AirportSerializer(airport)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "Sample airport",
            "closest_big_city": "Sample city",
        }
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airport(self):
        payload = {
            "name": "Sample airport",
            "closest_big_city": "Sample city",
        }
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.filter(name=payload["name"]).first()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airport, key))


def sample_route(**params):
    source = Airport.objects.create(
        name="Sample source", closest_big_city="Rome"
    )

    destination = Airport.objects.create(
        name="Sample destination", closest_big_city="Paris"
    )

    defaults = {
        "source": source,
        "destination": destination,
        "distance": 500,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_route_list(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        sample_route()
        sample_route()

        response = self.client.get(ROUTE_URL)

        routes = Route.objects.order_by("id")
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_route_detail(self):
        new_route = sample_route()
        url = reverse("airport:route-detail", args=[new_route.id])
        response = self.client.get(url)
        serializer = RouteListSerializer(new_route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_route_forbidden(self):
        new_payload = {
            "source": sample_airport().id,
            "destination": sample_airport().id,
            "distance": 1000,
        }
        response = self.client.post(ROUTE_URL, new_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_route(self):
        source = sample_airport()
        destination = sample_airport()
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 1000,
        }
        response = self.client.post(ROUTE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        route = Route.objects.filter(distance=payload["distance"]).first()
        serialized_route = RouteSerializer(route)
        for key in payload.keys():
            self.assertEqual(payload[key], serialized_route[key].value)


def sample_airplane_type(**params):
    defaults = {
        "name": "airplane_type 1",
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


class UnauthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_airplanetype_list(self):
        res = self.client.get(AIRPLANETYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane_types(self):
        AirplaneType.objects.create(name="Type 1")
        AirplaneType.objects.create(name="Type 2")

        response = self.client.get(AIRPLANETYPE_URL)

        airplane_types = AirplaneType.objects.order_by("id")
        new_serializer = AirplaneTypeSerializer(airplane_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_serializer.data)

    def test_retrieve_airplane_type_detail(self):
        airplane_type = AirplaneType.objects.create(name="Type 1")
        url = reverse("airport:airplanetype-detail", args=[airplane_type.id])
        response = self.client.get(url)

        serializer = AirplaneTypeSerializer(airplane_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airplane_type_forbidden(self):
        new_payload = {"name": "New Type"}
        response = self.client.post(AIRPLANETYPE_URL, new_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane_type(self):
        payload = {"name": "New Type"}
        res = self.client.post(AIRPLANETYPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane_type = AirplaneType.objects.filter(
            name=payload["name"]
        ).first()
        self.assertEqual(payload["name"], airplane_type.name)

    def test_update_airplane_type(self):
        airplane_type = AirplaneType.objects.create(name="Old Type")
        payload = {"name": "Updated Type"}
        url = reverse("airport:airplanetype-detail", args=[airplane_type.id])
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        airplane_type.refresh_from_db()
        self.assertEqual(payload["name"], airplane_type.name)

    def test_delete_airplanetype(self):
        airplane_type = AirplaneType.objects.create(name="Type to Delete")
        url = reverse("airport:airplanetype-detail", args=[airplane_type.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()

    defaults = {
        "airplane_type": airplane_type,
        "rows": 50,
        "seats_in_row": 6,
        "name": "Sample plane",
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_airplane_list(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        sample_airplane()

        response = self.client.get(AIRPLANE_URL)

        airplanes = Airplane.objects.order_by("id")
        serializer = AirplaneListSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_airplane_detail(self):
        new_airplane = sample_airplane()
        url = reverse("airport:airplane-detail", args=[new_airplane.id])
        response = self.client.get(url)
        serializer = AirplaneListSerializer(new_airplane)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airplane_forbidden(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "New Plane",
            "rows": 50,
            "seats_in_row": 6,
            "airplane_type": airplane_type.id,
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "New Plane",
            "rows": 50,
            "seats_in_row": 6,
            "airplane_type": airplane_type.id,
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.filter(name=payload["name"]).first()
        serialized_airplane = AirplaneSerializer(airplane)
        for key in payload.keys():
            self.assertEqual(payload[key], serialized_airplane[key].value)

    def test_update_airplane(self):
        airplane = sample_airplane()
        payload = {"name": "Updated Plane"}
        url = reverse("airport:airplane-detail", args=[airplane.id])
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        airplane.refresh_from_db()
        self.assertEqual(payload["name"], airplane.name)

    def test_delete_airplane(self):
        airplane = sample_airplane()
        url = reverse("airport:airplane-detail", args=[airplane.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    departure_time = timezone.make_aware(
        datetime.datetime.now(), timezone=timezone.get_current_timezone()
    )
    arrival_time = timezone.make_aware(
        datetime.datetime.now(), timezone=timezone.get_current_timezone()
    )
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_flight_list(self):
        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        sample_flight()
        sample_flight()

        response = self.client.get(FLIGHT_URL)

        flights = Flight.objects.order_by("id")
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_flight_detail(self):
        new_flight = sample_flight()
        url = reverse("airport:flight-detail", args=[new_flight.id])
        response = self.client.get(url)
        serializer = FlightListSerializer(new_flight)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_flight_forbidden(self):
        route = sample_route()
        airplane = sample_airplane()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2023-11-21T10:00:00Z",
            "arrival_time": "2023-11-21T14:00:00Z",
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self):
        route = sample_route()
        airplane = sample_airplane()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2023-11-21T10:00:00Z",
            "arrival_time": "2023-11-21T14:00:00Z",
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        flight = Flight.objects.filter(
            departure_time=payload["departure_time"]
        ).first()
        serialized_flight = FlightSerializer(flight)
        self.assertEqual(response.data, serialized_flight.data)


def sample_crew(**params):
    defaults = {
        "first_name": "first_name",
        "last_name": "last_name",
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_crew_list(self):
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_crews(self):
        sample_crew()
        sample_crew()
        response = self.client.get(CREW_URL)
        crews = Crew.objects.order_by("id")
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_crew_detail(self):
        new_crew = sample_crew()
        url = reverse("airport:crew-detail", args=[new_crew.id])
        response = self.client.get(url)
        serializer = CrewSerializer(new_crew)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_crew_forbidden(self):
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }
        response = self.client.post(CREW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }
        response = self.client.post(CREW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        crew = Crew.objects.filter(first_name=payload["first_name"]).first()
        serialized_crew = CrewSerializer(crew)
        self.assertEqual(response.data, serialized_crew.data)


def sample_flight_crew_member(**params):
    crew = sample_crew()
    flight = sample_flight()
    defaults = {
        "crew": crew,
        "flight": flight,
    }
    defaults.update(params)

    return FlightCrewMember.objects.create(**defaults)


class UnauthenticatedFlightCrewMemberApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_flight_crew_member_list(self):
        response = self.client.get(FLIGHT_CREW_MEMBER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightCrewMemberApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_flight_crew_members_forbidden(self):
        sample_flight_crew_member()
        sample_flight_crew_member()

        response = self.client.get(FLIGHT_CREW_MEMBER_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_flight_crew_member_detail_forbidden(self):
        new_flight_crew_member = sample_flight_crew_member()
        url = reverse(
            "airport:flightcrewmember-detail",
            args=[new_flight_crew_member.id],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_flight_crew_member_forbidden(self):
        flight = sample_flight()
        crew = sample_crew()
        payload = {
            "flight": flight.id,
            "crew": crew.id,
        }
        response = self.client.post(FLIGHT_CREW_MEMBER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightCrewMemberApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight_crew_member(self):
        flight = sample_flight()
        crew = sample_crew()
        payload = {
            "flight": flight.id,
            "crew": crew.id,
        }
        response = self.client.post(FLIGHT_CREW_MEMBER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        flight_crew_member = FlightCrewMember.objects.filter(
            crew=payload["crew"]
        ).first()
        serialized_flight_crew_member = FlightCrewMemberSerializer(
            flight_crew_member
        )
        self.assertEqual(response.data, serialized_flight_crew_member.data)


def sample_order(user=None, **params):
    created_at = timezone.make_aware(
        datetime.datetime.now(), timezone=timezone.get_current_timezone()
    )
    if not user:
        user = get_user_model().objects.create_user(
            f"test@testuser{random.randint(1, 2000)}.com",
            "testpass",
        )
    defaults = {
        "created_at": created_at,
        "user": user,
    }
    defaults.update(params)

    return Order.objects.create(**defaults)


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_order_list(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_orders_empty(self):
        sample_order()
        sample_order()

        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_retrieve_order_detail_forbidden(self):
        new_order = sample_order()
        url = reverse("airport:order-detail", args=[new_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_order_detail(self):
        new_order = sample_order(user=self.user)
        url = reverse("airport:order-detail", args=[new_order.id])
        response = self.client.get(url)
        serializer = OrderSerializer(new_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order(self):
        response = self.client.post(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_delete_order(self):
        new_order = sample_order()
        url = reverse("airport:order-detail", args=[new_order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
