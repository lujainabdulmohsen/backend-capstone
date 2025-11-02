from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import (
    GovernmentAgency,
    Service,
    ServiceRequest,
    Appointment,
    Document,
    BankAccount,
)
from datetime import date, time

User = get_user_model()


class ModelsTest(TestCase):
    def setUp(self):
        # إنشاء مستخدم تجريبي
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')

        # إنشاء وكالة حكومية
        self.agency = GovernmentAgency.objects.create(
            name='Ministry of Health',
            description='Handles all health related services'
        )

        # إنشاء خدمتين للوكالة
        self.service1 = Service.objects.create(
            agency=self.agency,
            name='Medical License Renewal',
            description='Renew your medical license online',
            fee=150.00
        )

        self.service2 = Service.objects.create(
            agency=self.agency,
            name='Hospital Registration',
            description='Register a new hospital or clinic',
            fee=250.00
        )

        # إنشاء طلبين لخدمة
        self.request1 = ServiceRequest.objects.create(
            user=self.user,
            service=self.service1,
            status=ServiceRequest.PENDING,
            payload={'field': 'value'}
        )

        self.request2 = ServiceRequest.objects.create(
            user=self.user,
            service=self.service2,
            status=ServiceRequest.APPROVED,
            payload={'field': 'another value'}
        )

        # إنشاء موعد (Appointment)
        self.appointment = Appointment.objects.create(
            service=self.service1,
            user=self.user,
            date=date(2025, 1, 1),
            time=time(10, 30),
            location='Riyadh Center'
        )

        # إنشاء وثيقة (Document)
        self.document = Document.objects.create(
            user=self.user,
            title='National ID',
            url='http://example.com/national-id.pdf'
        )

        # إنشاء حساب بنكي (BankAccount)
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            iban='SA1234567890123456789012',
            display_name='Primary Account',
            infinite_balance=True
        )
