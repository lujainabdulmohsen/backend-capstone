from rest_framework import serializers
from .models import GovernmentAgency, Service, ServiceRequest, Appointment


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
from django.contrib.auth.models import User
from rest_framework import serializers

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
