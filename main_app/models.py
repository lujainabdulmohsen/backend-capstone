from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GovernmentAgency(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    agency = models.ForeignKey(GovernmentAgency, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="requests")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payload = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Request #{self.id} - {self.service.name}"


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.date} {self.time}"


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=150)
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bank_account")
    iban = models.CharField(max_length=34, unique=True)
    display_name = models.CharField(max_length=100, default="Primary Account")
    infinite_balance = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.display_name}"
