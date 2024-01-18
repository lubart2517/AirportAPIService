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
    # Define fields to display in the admin interface here
    pass


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface here
    pass


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface here
    # Consider how to handle related fields like airplane, route, etc.
    pass


@admin.register(FlightCrewMember)
class FlightCrewMemberAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface here
    pass


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface here
    # Consider how to handle related fields like flight crew members
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface here
    # Consider how to handle related fields like tickets
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface here
    # Consider how to handle related fields like order, flight, etc.
    pass
