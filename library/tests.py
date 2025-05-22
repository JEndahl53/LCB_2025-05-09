# library/tests/test_organizations.py
from django.test import TestCase
from django.urls import reverse
from library.models import (
    Rental_Organization,
    Loaning_Organization,
    Borrowing_Organization,
)


class OrganizationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create instances for each organization type
        cls.rental_organization = Rental_Organization.objects.create(
            name="Rental Org",
            contact_name="John Doe",
            contact_email="rental@example.com",
            contact_phone="123-456-7890",
            website="https://rentalorg.com",
            notes="A rental organization.",
        )

        cls.loaning_organization = Loaning_Organization.objects.create(
            name="Loaning Org",
            contact_name="Jane Smith",
            contact_email="loaning@example.com",
            contact_phone="987-654-3210",
            website="https://loaningorg.com",
            notes="A loaning organization.",
        )

        cls.borrowing_organization = Borrowing_Organization.objects.create(
            name="Borrowing Org",
            contact_name="Chris Adams",
            contact_email="borrowing@example.com",
            contact_phone="456-789-0123",
            website="https://borrowingorg.com",
            notes="A borrowing organization.",
        )

    # Model Tests
    def test_rental_organization_str(self):
        self.assertEqual(str(self.rental_organization), "Rental Org")

    def test_loaning_organization_str(self):
        self.assertEqual(str(self.loaning_organization), "Loaning Org")

    def test_borrowing_organization_str(self):
        self.assertEqual(str(self.borrowing_organization), "Borrowing Org")

    def test_rental_organization_absolute_url(self):
        self.assertEqual(
            self.rental_organization.get_absolute_url(),
            reverse("rental_organization_detail", args=[self.rental_organization.id]),
        )

    def test_loaning_organization_absolute_url(self):
        self.assertEqual(
            self.loaning_organization.get_absolute_url(),
            reverse("loaning_organization_detail", args=[self.loaning_organization.id]),
        )

    def test_borrowing_organization_absolute_url(self):
        self.assertEqual(
            self.borrowing_organization.get_absolute_url(),
            reverse(
                "borrowing_organization_detail", args=[self.borrowing_organization.id]
            ),
        )

    # View Tests
    def test_rental_organization_list_view(self):
        response = self.client.get(reverse("rental_organization_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rental Org")

    def test_rental_organization_detail_view(self):
        response = self.client.get(
            reverse("rental_organization_detail", args=[self.rental_organization.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rental Org")
        self.assertContains(response, "John Doe")

    def test_rental_organization_create_view(self):
        response = self.client.post(
            reverse("rental_organization_create"),
            {
                "name": "New Rental Org",
                "contact_name": "Alice Doe",
                "contact_email": "new_rental@example.com",
                "contact_phone": "111-222-3333",
                "website": "https://newrental.org",
                "notes": "A new rental organization.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Rental_Organization.objects.filter(name="New Rental Org").exists()
        )

    def test_rental_organization_update_view(self):
        response = self.client.post(
            reverse("rental_organization_update", args=[self.rental_organization.id]),
            {
                "name": "Updated Rental Org",
                "contact_name": "John Updated",
                "contact_email": "updated_rental@example.com",
                "contact_phone": "123-456-7891",
                "website": "https://updatedrental.org",
                "notes": "An updated rental organization.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.rental_organization.refresh_from_db()
        self.assertEqual(self.rental_organization.name, "Updated Rental Org")

    def test_rental_organization_delete_view(self):
        response = self.client.post(
            reverse("rental_organization_delete", args=[self.rental_organization.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rental_Organization.objects.filter(name="Rental Org").exists())
