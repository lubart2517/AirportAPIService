from django.contrib import admin

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    FlightCrewMember,
    Crew,
    Order,
    Ticket
)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    pass


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass


@admin.register(FlightCrewMember)
class FlightCrewMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
