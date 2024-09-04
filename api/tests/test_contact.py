from unittest import mock

from django.test.utils import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


@override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
@override_settings(CONTACT_EMAIL="contact@example.com")
@override_settings(DEFAULT_FROM_EMAIL="from@example.com")
@mock.patch("api.views.contact.EmailMessage", autospec=True)
class TestContactView(APITestCase):
    def test_submit_contact_form(self, mocked_email):
        payload = {"name": "Anne Yversaire", "email": "anne@example.com", "message": "Hello world!"}

        self.client.post(reverse("api:contact"), payload, format="json")

        mocked_email.assert_called_once_with(
            subject="Demande de support de Anne Yversaire",
            body="Nom/Prénom\nAnne Yversaire\n------\n\nAdresse email\nanne@example.com\n------\n\nMessage\n« Hello world! »\n------",
            from_email="from@example.com",
            to=["contact@example.com"],
            reply_to=["anne@example.com"],
        )

    def test_missing_info(self, mocked_email):
        payload = {"name": "", "email": "anne@example.com", "message": "Hello world!"}

        response = self.client.post(reverse("api:contact"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mocked_email.assert_not_called()
