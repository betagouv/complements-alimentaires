import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.factories import DeclarantFactory, CompanySupervisorFactory
from django.contrib.auth import get_user_model
from data.factories.user import UserFactory

User = get_user_model()


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
        self.assertEqual(body.get("id"), authenticate.user.id)
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


class TestSignup(APITestCase):
    def setUp(self):
        self.user_data = dict(
            last_name="Cook", first_name="Tim", email="tim.cook@exemple.com", username="tcook", password="azerty123$"
        )
        self.url = reverse("api:signup")

    def test_signup_ok(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_id", response.data)
        new_user = User.objects.get(id=response.data["user_id"])
        self.assertEqual(new_user.email, self.user_data["email"])
        self.assertTrue(new_user.is_active)
        self.assertFalse(new_user.is_verified)
        self.assertFalse(new_user.is_superuser)
        self.assertFalse(new_user.is_staff)
        self.assertEqual(new_user.roles, [])

    def test_signup_with_existing_email(self):
        email = "eren@mikasa.com"
        UserFactory(email=email)
        self.user_data["email"] = email

        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["field_errors"])

    def test_signup_with_existing_username(self):
        username = "eren"
        UserFactory(username=username)
        self.user_data["username"] = username

        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data["field_errors"])

    def test_signup_with_invalid_password(self):
        self.user_data["password"] = "123"  # invalid
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["field_errors"])


class TestChangePassword(APITestCase):
    def setUp(self):
        self.url = reverse("api:change_password")
        self.password = "azerty123$"
        self.user = UserFactory(password=self.password)

    def test_change_password_ok(self):
        new_password = "azerty321$"
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, dict(old_password=self.password, new_password=new_password, confirm_new_password=new_password)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_with_invalid_old_password(self):
        new_password = "azerty321$"
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, dict(old_password="wrong-pasword", new_password=new_password, confirm_new_password=new_password)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data["field_errors"])

    def test_change_password_with_identical_new_password(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, dict(old_password=self.password, new_password=self.password, confirm_new_password=self.password)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data["field_errors"])

    def test_change_password_with_invalid_new_password(self):
        new_password = "a"
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, dict(old_password=self.password, new_password=new_password, confirm_new_password=new_password)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["non_field_errors"])  # Django default behaviour

    def test_change_password_with_wrong_confirm(self):
        new_password = "azerty321$"
        self.client.force_login(self.user)
        response = self.client.post(
            self.url,
            dict(old_password=self.password, new_password=new_password, confirm_new_password=new_password + "."),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_new_password", response.data["field_errors"])

    def test_change_password_unauthenticated(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestGenerateUsername(APITestCase):
    def test_generate_username(self):
        response = self.client.get(reverse("api:generate_username") + "?first_name=jean&last_name=dupon")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"username": "jean.dupon"})
