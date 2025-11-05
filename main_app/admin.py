from django.contrib import admin
from .models import GovernmentAgency, Service, CreditCard, ServiceRequest, Appointment, TrafficFine

@admin.register(GovernmentAgency)
class GovernmentAgencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("id",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "agency", "fee")
    list_filter = ("agency",)
    search_fields = ("name", "agency__name")
    ordering = ("id",)

admin.site.register(CreditCard)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("service__name", "user__username")
    ordering = ("-created_at",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "user", "date", "time", "location", "created_at")
    list_filter = ("date",)
    search_fields = ("service__name", "user__username")
    ordering = ("-created_at",)



from django.contrib import admin
from .models import TrafficFine

@admin.register(TrafficFine)
class TrafficFineAdmin(admin.ModelAdmin):
    list_display = ("fine_number", "user", "amount", "status", "issued_at", "due_date")
    list_filter = ("status", "issued_at", "violation_type")
    search_fields = ("fine_number", "user__username", "user__email", "violation_type")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "issued_at"
