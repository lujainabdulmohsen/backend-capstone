from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import GovernmentAgency, Service, ServiceRequest, Appointment, BankAccount
from .serializers import (
    GovernmentAgencySerializer,
    ServiceSerializer,
    ServiceRequestSerializer,
    AppointmentSerializer,
    UserSerializer,
)
import uuid
from rest_framework.permissions import IsAuthenticated


class AgencyList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        agencies = GovernmentAgency.objects.all()
        serializer = GovernmentAgencySerializer(agencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ServiceRequestList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = ServiceRequest.objects.filter(user=request.user).order_by("-created_at")
        serializer = ServiceRequestSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            bank_account = getattr(request.user, "bank_account", None)
            if not bank_account:
                return Response(
                    {"error": "No bank account found. Please create one first."},
                    status=status.HTTP_400_BAD_REQUEST
                )

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
                service = Service.objects.get(id=data["service_id"])
                instance = serializer.save(user=request.user)

                if "Appointment" in service.name or "Vaccination" in service.name or "Hospital" in service.name:
                    instance.status = "UPCOMING"
                elif "Fee" in service.name or "Passport" in service.name or "License" in service.name or "National ID" in service.name:
                    instance.status = "APPROVED"
                else:
                    instance.status = "PENDING"

                instance.save()
                serializer = ServiceRequestSerializer(instance)
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


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        iban = "SA" + str(uuid.uuid4().int)[:22]
        BankAccount.objects.create(
            user=user,
            iban=iban,
            display_name="Primary Account",
            infinite_balance=True
        )

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


class PayServiceRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        bank_account = request.user.bank_account
        if bank_account.infinite_balance:
            service_request.is_paid = True
            service_request.save()
            return Response({"message": "Payment successful (infinite balance)."}, status=status.HTTP_200_OK)
        return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)


class MyBankAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bank_account = request.user.bank_account
        data = {
            "iban": bank_account.iban,
            "display_name": bank_account.display_name,
            "infinite_balance": bank_account.infinite_balance
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        bank_account = request.user.bank_account
        display_name = request.data.get("display_name", bank_account.display_name)
        infinite_balance = request.data.get("infinite_balance", bank_account.infinite_balance)
        bank_account.display_name = display_name
        bank_account.infinite_balance = bool(infinite_balance)
        bank_account.save()
        data = {
            "iban": bank_account.iban,
            "display_name": bank_account.display_name,
            "infinite_balance": bank_account.infinite_balance
        }
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        bank_account = getattr(request.user, "bank_account", None)
        if bank_account:
            bank_account.delete()
            return Response(
                {"message": "Bank account deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "No bank account found for this user."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        if hasattr(request.user, "bank_account"):
            return Response({"error": "User already has a bank account."}, status=status.HTTP_400_BAD_REQUEST)
        iban = "SA" + str(uuid.uuid4().int)[:22]
        bank_account = BankAccount.objects.create(
            user=request.user,
            iban=iban,
            display_name=request.data.get("display_name", "Primary Account"),
            infinite_balance=request.data.get("infinite_balance", True)
        )
        data = {
            "iban": bank_account.iban,
            "display_name": bank_account.display_name,
            "infinite_balance": bank_account.infinite_balance
        }
        return Response(data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return Response({"error": "old_password and new_password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if not user.check_password(old_password):
            return Response({"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
