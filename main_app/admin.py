from django.contrib import admin
from .models import GovernmentAgency, Service, BankAccount, ServiceRequest, Appointment, Document

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

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "iban", "display_name", "infinite_balance")

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

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at")
    search_fields = ("title", "user__username")
    ordering = ("-created_at",)
