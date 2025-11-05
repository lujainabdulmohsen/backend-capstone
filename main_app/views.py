from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import GovernmentAgency, Service, ServiceRequest, Appointment, CreditCard, TrafficFine
from .serializers import (
    GovernmentAgencySerializer,
    ServiceSerializer,
    ServiceRequestSerializer,
    AppointmentSerializer,
    UserSerializer,
    TrafficFineSerializer,
    CreditCardSerializer
)
import uuid
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class HomeView(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the AI assistant api home route!'}
        return Response(content)


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
        print("this is the function we are testing")
        instance = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
        instance.delete()
        return Response({ "success": True }, status=status.HTTP_200_OK)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
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
        except Exception as err:
            print(str(err))
            return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        try:
            card = CreditCard.objects.filter(user=request.user).first()
            if card:
                service_request = get_object_or_404(ServiceRequest, pk=pk, user=request.user)
                service_request.is_paid = True
                service_request.status = "APPROVED"
                service_request.save()
                return Response({"message": "Payment successful (infinite balance)."}, status=status.HTTP_200_OK)
        except Exception as err:
            print(str(err))
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyBankAccountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreditCardSerializer

    def get(self, request):
        try:
            card = CreditCard.objects.filter(user=request.user).first()

            if card:
                serializer = self.serializer_class(card)
                return Response({ "acct": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({ "acct": None}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            card = CreditCard.objects.filter(user=request.user).first()
            serializer = self.serializer_class(card, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:

            existing_creditcard = CreditCard.objects.filter(user=request.user)
            if existing_creditcard:
                existing_creditcard.delete()
                return Response({"ok": "Bank account deleted successfully."}, status=status.HTTP_200_OK)
            return Response({ "success": True}, status=status.HTTP_200_OK)
        except Exception as err:
            print(str(err))
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request):
        try:
            
            existing_creditcard = CreditCard.objects.filter(user=request.user)
            if existing_creditcard:
                existing_creditcard.delete()

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(str(err))
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class MyFinesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fines = TrafficFine.objects.filter(user=request.user).exclude(status=TrafficFine.PAID).order_by("-issued_at", "-created_at")
        serializer = TrafficFineSerializer(fines, many=True)
        return Response({"fines": serializer.data}, status=status.HTTP_200_OK)


class PayFinesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        with transaction.atomic():
            pay_all = data.get("pay_all") or data.get("payAll")
            fine_ids = data.get("fine_ids") or data.get("fineIds")

            if pay_all:
                fines_qs = TrafficFine.objects.filter(user=user).exclude(status=TrafficFine.PAID)
            else:
                if not isinstance(fine_ids, list) or not fine_ids:
                    return Response({"detail": "fine_ids required"}, status=status.HTTP_400_BAD_REQUEST)
                fines_qs = TrafficFine.objects.filter(user=user, id__in=fine_ids).exclude(status=TrafficFine.PAID)

            if not fines_qs.exists():
                return Response({"detail": "No matching unpaid fines found."}, status=status.HTTP_400_BAD_REQUEST)

            updated_count = fines_qs.update(status=TrafficFine.PAID)

            for fine in fines_qs:
                ServiceRequest.objects.create(
                    user=user,
                    service=None,
                    payload={
                        "fine_number": fine.fine_number,
                        "amount": str(fine.amount),
                        "violation_type": fine.violation_type,
                    },
                    status="APPROVED",
                    is_paid=True
                )

        fines = TrafficFine.objects.filter(user=user).exclude(status=TrafficFine.PAID).order_by("-issued_at", "-created_at")
        serializer = TrafficFineSerializer(fines, many=True)
        return Response(
            {"detail": f"{updated_count} fine(s) marked as PAID and logged to My Requests.", "fines": serializer.data},
            status=status.HTTP_200_OK
        )
