import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.factories import DeclarantFactory, CompanySupervisorFactory


class TestLoggedUserApi(APITestCase):
    def test_unauthenticated_logged_user_call(self):
        """
        When calling this API unathenticated we expect a 204
        """
        response = self.client.get(reverse("api:logged_user"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_authenticated_logged_user_call(self):
        """
        When calling this API authenticated we expect to get a
        JSON representation of the authenticated user
        """
        response = self.client.get(reverse("api:logged_user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertEqual(body.get("username"), authenticate.user.username)
        self.assertEqual(body.get("email"), authenticate.user.email)
        self.assertEqual(body.get("firstName"), authenticate.user.first_name)
        self.assertEqual(body.get("lastName"), authenticate.user.last_name)
        self.assertEqual(body.get("roles"), [])
        self.assertIn("id", body)

    @authenticate
    def test_authenticated_logged_user_call_with_roles(self):
        """Ensure that roles are added to the JSON representation of the user"""

        def _get_role_names(resp):
            return {role["name"] for role in resp.data["roles"]}

        # Without role
        response = self.client.get(reverse("api:logged_user"))
        self.assertEqual(_get_role_names(response), set())

        # With two roles
        DeclarantFactory(user=authenticate.user)
        CompanySupervisorFactory(user=authenticate.user)

        response = self.client.get(reverse("api:logged_user"))
        self.assertEqual(_get_role_names(response), {"Declarant", "CompanySupervisor"})


class TestGenerateUsername(APITestCase):
    def test_generate_username(self):
        response = self.client.get(reverse("api:generate_username") + "?first_name=jean&last_name=dupon")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"username": "jean.dupon"})
