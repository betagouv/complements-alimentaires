from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import IngredientFactory, PlantFactory
from data.models import ErrorReport

from .utils import authenticate


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TestErrorReport(APITestCase):
    def setUp(self):
        self.plant = PlantFactory()
        self.ingredient = IngredientFactory()
        mail.outbox = []

    def test_error_report_not_logged_in(self):
        payload = {
            "email": "example@foo.com",
            "message": "hello world",
            "plant": self.plant.id,
        }

        response = self.client.post(reverse("api:report_issue"), payload, format="json")
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        error_report = ErrorReport.objects.get(pk=body["id"])
        self.assertEqual(error_report.email, "example@foo.com")
        self.assertEqual(error_report.plant, self.plant)
        self.assertIsNone(error_report.ingredient)
        self.assertIsNone(error_report.microorganism)
        self.assertIsNone(error_report.substance)
        self.assertIsNone(error_report.author)
        self.assertEqual(error_report.status, ErrorReport.Status.NEW)

        # Email sending
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Nouvelle incohérence remontée dans la base ingrédients")
        self.assertIn("example@foo.com", mail.outbox[0].body)

    def test_error_report_without_email(self):
        payload = {
            "message": "hello world",
            "plant": self.plant.id,
        }

        response = self.client.post(reverse("api:report_issue"), payload, format="json")
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        error_report = ErrorReport.objects.get(pk=body["id"])
        self.assertEqual(error_report.email, "")

        # Email sending
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Nouvelle incohérence remontée dans la base ingrédients")
        self.assertIn("Un utilisateur anonyme", mail.outbox[0].body)

    @authenticate
    def test_error_report_logged_in(self):
        payload = {
            "message": "hello world",
            "ingredient": self.ingredient.id,
        }

        response = self.client.post(reverse("api:report_issue"), payload, format="json")
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        error_report = ErrorReport.objects.get(pk=body["id"])
        self.assertEqual(error_report.author, authenticate.user)

        # Email sending
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Nouvelle incohérence remontée dans la base ingrédients")
        self.assertIn(f"{authenticate.user.name} ({authenticate.user.email})", mail.outbox[0].body)
