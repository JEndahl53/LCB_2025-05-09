# concerts/tests.py
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import Conductor, Guest
from .views import (
    ConductorListView,
    ConductorDetailView,
    ConductorCreateView,
    ConductorUpdateView,
    ConductorDeleteView,
    GuestListView,
    GuestDetailView,
    GuestCreateView,
    GuestUpdateView,
    GuestDeleteView,
)


class ConductorModelTest(TestCase):
    """Test case for the Conductor model"""

    def setUp(self):
        self.conductor = Conductor.objects.create(
            first_name="Leonard",
            last_name="Bernstein",
            middle_initial="B",
            honorific="Maestro",
            description="American conductor, composer, and pianist.",
        )

    def test_conductor_creation(self):
        """Test creating a conductor instance"""
        self.assertEqual(self.conductor.first_name, "Leonard")
        self.assertEqual(self.conductor.last_name, "Bernstein")
        self.assertEqual(self.conductor.middle_initial, "B")
        self.assertEqual(self.conductor.honorific, "Maestro")
        self.assertEqual(
            self.conductor.description, "American conductor, composer, and pianist."
        )

    def test_conductor_str(self):
        """Test the string representation of a conductor"""
        self.assertEqual(str(self.conductor), "Bernstein, Leonard")

    def test_conductor_get_full_name(self):
        """Test the get_full_name method"""
        self.assertEqual(self.conductor.get_full_name(), "Leonard Bernstein")

    def test_conductor_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.conductor.get_absolute_url(),
            f"/concerts/conductors/{self.conductor.id}/",
        )


class GuestModelTest(TestCase):
    """Test case for the Guest model"""

    def setUp(self):
        self.guest = Guest.objects.create(
            first_name="Yo-Yo", last_name="Ma", instrument="Cello"
        )

    def test_guest_creation(self):
        """Test creating a guest instance"""
        self.assertEqual(self.guest.first_name, "Yo-Yo")
        self.assertEqual(self.guest.last_name, "Ma")
        self.assertEqual(self.guest.instrument, "Cello")

    def test_guest_str(self):
        """Test the string representation of a guest"""
        self.assertEqual(str(self.guest), "Ma, Yo-Yo")

    def test_guest_get_full_name(self):
        """Test the get_full_name method"""
        self.assertEqual(self.guest.get_full_name(), "Yo-Yo Ma")

    def test_guest_get_absolute_url(self):
        """Test the get_absolute_url method"""
        self.assertEqual(
            self.guest.get_absolute_url(), f"/concerts/guests/{self.guest.id}/"
        )


class ConductorViewsTest(TestCase):
    """Test case for the Conductor views"""

    def setUp(self):
        self.client = Client()
        self.conductor = Conductor.objects.create(
            first_name="Leonard", last_name="Bernstein"
        )
        self.list_url = reverse("conductor_list")
        self.detail_url = reverse("conductor_detail", args=[self.conductor.id])
        self.create_url = reverse("conductor_create")
        self.update_url = reverse("conductor_update", args=[self.conductor.id])
        self.delete_url = reverse("conductor_delete", args=[self.conductor.id])

    def test_conductor_list_view(self):
        """Test that list view returns correct status code and template"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_list.html")
        self.assertContains(response, self.conductor.get_full_name())

    def test_conductor_detail_view(self):
        """Test that detail view returns correct status code and template"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_detail.html")
        self.assertContains(response, self.conductor.get_full_name())

    def test_conductor_create_view(self):
        """Test that create view returns correct status code and template"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_conductor_create_view_post(self):
        """Test creating a new conductor via POST"""
        data = {
            "first_name": "Gustav",
            "last_name": "Mahler",
            "middle_initial": "M",
            "honorific": "Herr",
            "description": "Austrian composer and conductor",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(Conductor.objects.count(), 2)
        self.assertRedirects(response, self.list_url)

    def test_conductor_update_view(self):
        """Test that update view returns correct status code and template"""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_conductor_update_view_post(self):
        """Test updating a conductor via POST"""
        data = {
            "first_name": "Leonard",
            "last_name": "Bernstein",
            "middle_initial": "L",
            "honorific": "Dr.",
            "description": "Updated description",
        }
        response = self.client.post(self.update_url, data)
        self.conductor.refresh_from_db()
        self.assertEqual(self.conductor.middle_initial, "L")
        self.assertEqual(self.conductor.honorific, "Dr.")
        self.assertEqual(self.conductor.description, "Updated description")
        self.assertRedirects(response, self.list_url)

    def test_conductor_delete_view(self):
        """Test that delete view returns correct status code and template"""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_confirm_delete.html")

    def test_conductor_delete_view_post(self):
        """Test deleting a conductor via POST"""
        response = self.client.post(self.delete_url)
        self.assertEqual(Conductor.objects.count(), 0)
        self.assertRedirects(response, self.list_url)

    def test_conductor_model_name_context(self):
        """Test that context has correct model name variables"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.context["view"].get_model_verbose_name(), "Conductor")
        self.assertEqual(response.context["view"].get_model_name_for_url(), "conductor")


class GuestViewsTest(TestCase):
    """Test case for the Guest views"""

    def setUp(self):
        self.client = Client()
        self.guest = Guest.objects.create(
            first_name="Yo-Yo", last_name="Ma", instrument="Cello"
        )
        self.list_url = reverse("guest_list")
        self.detail_url = reverse("guest_detail", args=[self.guest.id])
        self.create_url = reverse("guest_create")
        self.update_url = reverse("guest_update", args=[self.guest.id])
        self.delete_url = reverse("guest_delete", args=[self.guest.id])

    def test_guest_list_view(self):
        """Test that list view returns correct status code and template"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_list.html")
        self.assertContains(response, self.guest.get_full_name())

    def test_guest_detail_view(self):
        """Test that detail view returns correct status code and template"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_detail.html")
        self.assertContains(response, self.guest.get_full_name())

    def test_guest_create_view(self):
        """Test that create view returns correct status code and template"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_guest_create_view_post(self):
        """Test creating a new guest via POST"""
        data = {
            "first_name": "Itzhak",
            "last_name": "Perlman",
            "instrument": "Violin",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(Guest.objects.count(), 2)
        self.assertRedirects(response, self.list_url)

    def test_guest_update_view(self):
        """Test that update view returns correct status code and template"""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_form.html")

    def test_guest_update_view_post(self):
        """Test updating a guest via POST"""
        data = {
            "first_name": "Yo-Yo",
            "last_name": "Ma",
            "instrument": "Double Bass",
        }
        response = self.client.post(self.update_url, data)
        self.guest.refresh_from_db()
        self.assertEqual(self.guest.instrument, "Double Bass")
        self.assertRedirects(response, self.list_url)

    def test_guest_delete_view(self):
        """Test that delete view returns correct status code and template"""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "people/person_confirm_delete.html")

    def test_guest_delete_view_post(self):
        """Test deleting a guest via POST"""
        response = self.client.post(self.delete_url)
        self.assertEqual(Guest.objects.count(), 0)
        self.assertRedirects(response, self.list_url)

    def test_guest_model_name_context(self):
        """Test that context has correct model name variables"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.context["view"].get_model_verbose_name(), "Guest")
        self.assertEqual(response.context["view"].get_model_name_for_url(), "guest")


class URLsTest(TestCase):
    """Test case for URL resolution"""

    def test_conductor_urls(self):
        """Test that conductor URLs resolve to the correct views"""
        self.assertEqual(
            resolve("/concerts/conductors/").func.view_class, ConductorListView
        )
        self.assertEqual(
            resolve("/concerts/conductors/1/").func.view_class, ConductorDetailView
        )
        self.assertEqual(
            resolve("/concerts/conductors/create/").func.view_class, ConductorCreateView
        )
        self.assertEqual(
            resolve("/concerts/conductors/1/update/").func.view_class,
            ConductorUpdateView,
        )
        self.assertEqual(
            resolve("/concerts/conductors/1/delete/").func.view_class,
            ConductorDeleteView,
        )

    def test_guest_urls(self):
        """Test that guest URLs resolve to the correct views"""
        self.assertEqual(resolve("/concerts/guests/").func.view_class, GuestListView)
        self.assertEqual(
            resolve("/concerts/guests/1/").func.view_class, GuestDetailView
        )
        self.assertEqual(
            resolve("/concerts/guests/create/").func.view_class, GuestCreateView
        )
        self.assertEqual(
            resolve("/concerts/guests/1/update/").func.view_class, GuestUpdateView
        )
        self.assertEqual(
            resolve("/concerts/guests/1/delete/").func.view_class, GuestDeleteView
        )


class TemplateContextTest(TestCase):
    """Test case for template context variables"""

    def setUp(self):
        self.client = Client()
        self.conductor = Conductor.objects.create(
            first_name="Leonard", last_name="Bernstein"
        )
        self.guest = Guest.objects.create(
            first_name="Yo-Yo", last_name="Ma", instrument="Cello"
        )

    def test_conductor_delete_view_context(self):
        """Test that the delete view provides model_name_for_url in context"""
        response = self.client.get(
            reverse("conductor_delete", args=[self.conductor.id])
        )
        self.assertIn("model_name_for_url", response.context)
        self.assertEqual(response.context["model_name_for_url"], "conductor")
        self.assertIn("person", response.context)
        self.assertEqual(response.context["person"], self.conductor)

    def test_guest_delete_view_context(self):
        """Test that the delete view provides model_name_for_url in context"""
        response = self.client.get(reverse("guest_delete", args=[self.guest.id]))
        self.assertIn("model_name_for_url", response.context)
        self.assertEqual(response.context["model_name_for_url"], "guest")
        self.assertIn("person", response.context)
        self.assertEqual(response.context["person"], self.guest)
