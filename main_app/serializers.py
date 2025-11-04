from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GovernmentAgency, Service, ServiceRequest, Appointment, TrafficFine


class GovernmentAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentAgency
        fields = ["id", "name", "description"]


class ServiceSerializer(serializers.ModelSerializer):
    agency = GovernmentAgencySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ["id", "name", "description", "fee", "agency"]


class ServiceRequestSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service", write_only=True
    )

    class Meta:
        model = ServiceRequest
        fields = [
            "id",
            "created_at",
            "status",
            "payload",
            "service",
            "service_id",
            "user",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service", write_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "date",
            "time",
            "location",
            "created_at",
            "service",
            "service_id",
            "user",
        ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class TrafficFineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFine
        fields = ["id", "fine_number", "amount", "violation_type", "issued_at", "due_date", "status", "notes"]
