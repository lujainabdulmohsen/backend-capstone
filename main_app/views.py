from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import GovernmentAgency, Service, ServiceRequest, Appointment
from .serializers import (
    GovernmentAgencySerializer,
    ServiceSerializer,
    ServiceRequestSerializer,
    AppointmentSerializer,
    UserSerializer,
)

# ==============================
# 🔹 Agencies
# ==============================
class AgencyList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        agencies = GovernmentAgency.objects.all()
        serializer = GovernmentAgencySerializer(agencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================
# 🔹 Services
# ==============================
class ServiceList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        services = Service.objects.all().order_by("id")
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================
# 🔹 Service Requests (User-Specific)
# ==============================
class ServiceRequestList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = ServiceRequest.objects.filter(user=request.user).order_by("-created_at")
        serializer = ServiceRequestSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data.copy()
            service_id = data.get("service_id") or data.get("service")
            if not service_id:
                return Response({"error": "Service ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            data["service_id"] = service_id
            data.pop("service", None)

            payload = data.get("payload")
            if not payload:
                payload = {}
            elif isinstance(payload, str):
                import json
                try:
                    payload = json.loads(payload)
                except:
                    payload = {}

            data["payload"] = payload
            data["user"] = request.user.id

            serializer = ServiceRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceRequestDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        instance = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        serializer = ServiceRequestSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        serializer = ServiceRequestSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==============================
# 🔹 Authentication Views
# ==============================
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
