# concerts/tests.py
from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import Conductor, Guest, Venue
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
    VenueListView,
    VenueDetailView,
    VenueCreateView,
    VenueUpdateView,
    VenueDeleteView,
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


class VenueModelTest(TestCase):
    """Test case for the Venue model"""

    def setUp(self):
        self.venue = Venue.objects.create(
            name="Symphony Hall",
            address="301 Massachusetts Ave",
            city="Boston",
            state="MA",
            zip_code="02115",
        )

    def test_venue_creation(self):
        """Test creating a venue instance"""
        self.assertEqual(self.venue.name, "Symphony Hall")
        self.assertEqual(self.venue.address, "301 Massachusetts Ave")
        self.assertEqual(self.venue.city, "Boston")
        self.assertEqual(self.venue.state, "MA")
        self.assertEqual(self.venue.zip_code, "02115")

    def test_venue_str(self):
        """Test the string representation of a venue"""
        self.assertEqual(str(self.venue), "Symphony Hall")

    def test_venue_get_absolute_url(self):
        """Test the get_absolute_url method"""
        expected_url = reverse("venue_detail", args=[self.venue.id])
        self.assertEqual(self.venue.get_absolute_url(), expected_url)

    def test_venue_full_address(self):
        """Test the venue's full address property"""
        expected_address = "301 Massachusetts Ave, Boston, MA 02115"
        # Assuming you have a full_address property or method
        # If you don't, consider adding one!
        if hasattr(self.venue, "full_address"):
            self.assertEqual(self.venue.full_address, expected_address)


class VenueViewsTest(TestCase):
    """Test case for the Venue views"""

    def setUp(self):
        self.client = Client()
        self.venue = Venue.objects.create(
            name="Symphony Hall",
            address="301 Massachusetts Ave",
            city="Boston",
            state="MA",
            zip_code="02115",
        )
        self.list_url = reverse("venue_list")
        self.detail_url = reverse("venue_detail", args=[self.venue.id])
        self.create_url = reverse("venue_create")
        self.update_url = reverse("venue_update", args=[self.venue.id])
        self.delete_url = reverse("venue_delete", args=[self.venue.id])

    def test_venue_list_view(self):
        """Test that list view returns correct status code and template"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "venue/venue_list.html")
        self.assertContains(response, self.venue.name)
        # Check that the venues are in the context
        self.assertIn("venues", response.context)

    def test_venue_detail_view(self):
        """Test that detail view returns correct status code and template"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "venue/venue_detail.html")
        self.assertContains(response, self.venue.name)
        # Check that the venue is in the context
        self.assertEqual(response.context["venue"], self.venue)

    def test_venue_create_view(self):
        """Test that create view returns correct status code and template"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "venue/venue_form.html")

    def test_venue_create_view_post(self):
        """Test creating a new venue via POST"""
        data = {
            "name": "Carnegie Hall",
            "address": "881 7th Ave",
            "city": "New York",
            "state": "NY",
            "zip_code": "10019",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(Venue.objects.count(), 2)
        new_venue = Venue.objects.get(name="Carnegie Hall")
        self.assertEqual(new_venue.city, "New York")
        # Check redirect after create
        self.assertRedirects(response, reverse("venue_list")

    def test_venue_update_view(self):
        """Test that update view returns correct status code and template"""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "venue/venue_form.html")
        # Check form is pre-populated with venue data
        self.assertContains(response, self.venue.name)
        self.assertContains(response, self.venue.city)

    def test_venue_update_view_post(self):
        """Test updating a venue via POST"""
        data = {
            "name": "Symphony Hall",
            "address": "301 Massachusetts Ave",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02115",
        }
        response = self.client.post(self.update_url, data)
        self.venue.refresh_from_db()
        # Check redirect after update
        self.assertRedirects(response, reverse("venue_detail", args=[self.venue.id]))

    def test_venue_delete_view(self):
        """Test that delete view returns correct status code and template"""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "venue/venue_confirm_delete.html")
        self.assertContains(response, self.venue.name)

    def test_venue_delete_view_post(self):
        """Test deleting a venue via POST"""
        response = self.client.post(self.delete_url)
        self.assertEqual(Venue.objects.count(), 0)
        # Check redirect after delete
        self.assertRedirects(response, self.list_url)

    def test_venue_form_errors(self):
        """Test form validation errors"""
        # Missing required field 'name'
        data = {
            "address": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)  # Stays on the form page
        self.assertFormError(response, "form", "name", "This field is required.")


class VenueUrlsTest(TestCase):
    """Test case for URL resolution"""

    def test_venue_list_url_resolves(self):
        url = reverse("venue_list")
        self.assertEqual(resolve(url).func.view_class, VenueListView)

    def test_venue_detail_url_resolves(self):
        url = reverse("venue_detail", args=[1])
        self.assertEqual(resolve(url).func.view_class, VenueDetailView)

    def test_venue_create_url_resolves(self):
        url = reverse("venue_create")
        self.assertEqual(resolve(url).func.view_class, VenueCreateView)

    def test_venue_update_url_resolves(self):
        url = reverse("venue_update", args=[1])
        self.assertEqual(resolve(url).func.view_class, VenueUpdateView)

    def test_venue_delete_url_resolves(self):
        url = reverse("venue_delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, VenueDeleteView)


class VenueCrispyFormTest(TestCase):
    """Test case for crispy form functionality"""

    def test_venue_form_has_crispy_fields(self):
        """Test that the form uses crispy fields correctly"""
        response = self.client.get(reverse("venue_create"))
        self.assertEqual(response.status_code, 200)

        # Check that crispy form tag is present
        self.assertContains(response, "csrfmiddlewaretoken")

        # Check that form is using crispy styling
        # These checks may need to be adjusted based on the specific HTML output of crispy-tailwind
        self.assertContains(response, 'class="')

        # Check for some common field names that would be in the form
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, 'id="id_address"')
        self.assertContains(response, 'id="id_city"')


class VenueIntegrationTest(TestCase):
    """Test case for testing venue workflows end-to-end"""

    def test_venue_create_edit_delete_workflow(self):
        """Test the full workflow of creating, editing, and deleting a venue"""
        client = Client()

        # Step 1: Create a new venue
        create_data = {
            "name": "New Test Venue",
            "address": "123 Test St",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
        }
        response = client.post(reverse("venue_create"), create_data)
        self.assertEqual(Venue.objects.count(), 1)
        venue = Venue.objects.first()
        self.assertEqual(venue.name, "New Test Venue")

        # Step 2: Edit the venue
        update_data = {
            "name": "Updated Test Venue",
            "address": "123 Test St",
            "city": "Testville",
            "state": "TS",
            "zip_code": "12345",
        }
        response = client.post(reverse("venue_update", args=[venue.id]), update_data)
        venue.refresh_from_db()
        self.assertEqual(venue.name, "Updated Test Venue")

        # Step 3: View the venue details
        response = client.get(reverse("venue_detail", args=[venue.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Updated Test Venue")

        # Step 4: Delete the venue
        response = client.post(reverse("venue_delete", args=[venue.id]))
        self.assertEqual(Venue.objects.count(), 0)

        # Step 5: Check that we can't access the venue anymore
        response = client.get(reverse("venue_detail", args=[venue.id]))
        self.assertEqual(response.status_code, 404)
