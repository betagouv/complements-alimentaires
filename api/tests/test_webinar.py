from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import WebinarFactory


class TestWebinarAPI(APITestCase):
    def test_webinaire_format(self):
        """
        Test correct data returned by API
        """
        today = timezone.now()
        WebinarFactory.create(end_date=today)

        response = self.client.get(reverse("webinar_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        webinaire = body[0]
        self.assertIn("id", webinaire)
        self.assertIn("title", webinaire)
        self.assertIn("tagline", webinaire)
        self.assertIn("startDate", webinaire)
        self.assertIn("endDate", webinaire)
        self.assertIn("link", webinaire)

    def test_get_upcoming_webinaires(self):
        """
        The API should only return upcoming community events
        """
        today = timezone.now()
        # past community event
        WebinarFactory.create(end_date=(today - timedelta(days=1)))

        upcoming_webinaires = [
            WebinarFactory.create(start_date=(today + timedelta(days=9)), end_date=(today + timedelta(days=10))),
            WebinarFactory.create(start_date=today, end_date=(today + timedelta(hours=1))),
            WebinarFactory.create(start_date=(today + timedelta(days=8)), end_date=(today + timedelta(days=20))),
        ]

        response = self.client.get(reverse("webinar_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
        # webinaires should be returned in ascending start date order
        self.assertEqual(body[0]["id"], upcoming_webinaires[1].id)
        self.assertEqual(body[1]["id"], upcoming_webinaires[2].id)
        self.assertEqual(body[2]["id"], upcoming_webinaires[0].id)
