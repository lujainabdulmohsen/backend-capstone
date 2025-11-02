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
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')
        self.agency = GovernmentAgency.objects.create(
            name='Ministry of Health',
            description='Handles all health related services'
        )
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
        self.appointment = Appointment.objects.create(
            service=self.service1,
            user=self.user,
            date=date(2025, 1, 1),
            time=time(10, 30),
            location='Riyadh Center'
        )
        self.document = Document.objects.create(
            user=self.user,
            title='National ID',
            url='http://example.com/national-id.pdf'
        )
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            iban='SA1234567890123456789012',
            display_name='Primary Account',
            infinite_balance=True
        )

    def test_user_create(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_agency_create(self):
        self.assertEqual(str(self.agency), 'Ministry of Health')

    def test_service_create(self):
        self.assertEqual(str(self.service1), 'Medical License Renewal')
        self.assertEqual(str(self.service2), 'Hospital Registration')

    def test_service_request_create(self):
        expected_str1 = f"Request #{self.request1.id} - {self.service1.name}"
        expected_str2 = f"Request #{self.request2.id} - {self.service2.name}"
        self.assertEqual(str(self.request1), expected_str1)
        self.assertEqual(str(self.request2), expected_str2)

    def test_appointment_create(self):
        expected_str = f"{self.service1.name} - {self.appointment.date} {self.appointment.time}"
        self.assertEqual(str(self.appointment), expected_str)

    def test_document_create(self):
        self.assertEqual(str(self.document), 'National ID')

    def test_bank_account_create(self):
        expected_str = f"{self.user.username} - {self.bank_account.display_name}"
        self.assertEqual(str(self.bank_account), expected_str)

    def test_service_belongs_to_agency(self):
        self.assertEqual(self.service1.agency, self.agency)
        self.assertEqual(self.service2.agency.name, 'Ministry of Health')

    def test_service_request_relationships(self):
        self.assertEqual(self.request1.user, self.user)
        self.assertEqual(self.request1.service, self.service1)
        self.assertEqual(self.request2.service.agency, self.agency)

    def test_appointment_relationships(self):
        self.assertEqual(self.appointment.user.username, 'testuser')
        self.assertEqual(self.appointment.service.name, 'Medical License Renewal')

    def test_document_relationships(self):
        self.assertEqual(self.document.user, self.user)

    def test_bank_account_relationships(self):
        self.assertEqual(self.bank_account.user.email, 'test@example.com')
        self.assertTrue(hasattr(self.user, 'bank_account'))

    def test_service_request_ordering_by_creation(self):
        requests = list(ServiceRequest.objects.order_by('-created_at'))
        self.assertGreaterEqual(requests[0].created_at, requests[1].created_at)

    def test_appointments_order_by_date(self):
        appointment2 = Appointment.objects.create(
            service=self.service2,
            user=self.user,
            date=date(2025, 2, 1),
            time=time(9, 0),
            location='Jeddah Center'
        )
        appointments = list(Appointment.objects.order_by('date'))
        self.assertLessEqual(appointments[0].date, appointments[1].date)

    def test_deleting_user_cascades_to_related_models(self):
        self.user.delete()
        self.assertEqual(ServiceRequest.objects.count(), 0)
        self.assertEqual(Appointment.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(BankAccount.objects.count(), 0)

    def test_deleting_agency_cascades_to_services(self):
        self.agency.delete()
        self.assertEqual(Service.objects.count(), 0)

    def test_deleting_service_cascades_to_requests_and_appointments(self):
        service_id = self.service1.id
        self.service1.delete()
        self.assertEqual(ServiceRequest.objects.filter(service_id=service_id).count(), 0)
        self.assertEqual(Appointment.objects.filter(service_id=service_id).count(), 0)
