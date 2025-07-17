from unittest import mock

from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from rest_framework import status

from data.factories import (
    CompanyFactory,
    ControlRoleFactory,
    DeclarantRoleFactory,
    InstructionRoleFactory,
    SupervisorRoleFactory,
    VisaRoleFactory,
)
from data.factories.user import UserFactory

from .utils import ProjectAPITestCase

User = get_user_model()


class TestGetLoggedUser(ProjectAPITestCase):
    viewname = "get_logged_user"

    def test_unauthenticated_logged_user_call(self):
        """
        When calling this API unathenticated we expect a 204
        """
        response = self.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_logged_user_call(self):
        """
        When calling this API authenticated we expect to get a
        JSON representation of the authenticated user
        """
        user = self.login()
        response = self.get(self.url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), user.id)
        self.assertEqual(response.data.get("username"), user.username)
        self.assertEqual(response.data.get("email"), user.email)
        self.assertEqual(response.data.get("first_name"), user.first_name)
        self.assertEqual(response.data.get("last_name"), user.last_name)
        self.assertEqual(response.data.get("companies"), [])
        self.assertIn("id", response.data)

    def test_authenticated_logged_user_call_with_roles(self):
        """Ensure that roles are added to the JSON representation of the user"""

        company_1 = CompanyFactory()
        company_2 = CompanyFactory()
        CompanyFactory()  # une autre entreprise qui ne sera liée à personne

        user = self.login()

        # Without role in any company
        response = self.get(self.url())
        self.assertEqual(response.data["companies"], [])

        # With 3 roles in 2 companies
        declarant_role = DeclarantRoleFactory(user=user, company=company_1)
        supervisor_role_1 = SupervisorRoleFactory(user=user, company=company_1)
        supervisor_role_2 = SupervisorRoleFactory(user=user, company=company_2)

        response = self.get(self.url())
        companies = response.data["companies"]
        self.assertEqual(len(companies), 2)
        self.assertEqual(len(list(filter(lambda x: x["id"] == company_1.id, companies))), 1)
        self.assertEqual(len(list(filter(lambda x: x["id"] == company_2.id, companies))), 1)

        json_company_1 = next(filter(lambda x: x["id"] == company_1.id, companies))
        json_company_2 = next(filter(lambda x: x["id"] == company_2.id, companies))

        self.assertCountEqual(
            json_company_1["roles"],
            [
                {"id": supervisor_role_1.id, "name": "SupervisorRole"},
                {"id": declarant_role.id, "name": "DeclarantRole"},
            ],
        )
        self.assertCountEqual(json_company_2["roles"], [{"id": supervisor_role_2.id, "name": "SupervisorRole"}])

    def test_global_roles(self):
        """
        Les rôles globaux sont serialisées dans le call du logged user
        """
        user = self.login()
        InstructionRoleFactory(user=user)
        response = self.get(self.url()).json()

        self.assertEqual(len(response["globalRoles"]), 1)
        self.assertEqual(response["globalRoles"][0]["name"], "InstructionRole")

    def test_visa_roles(self):
        """
        Les rôles du visa sont serialisées dans le call du logged user
        """
        user = self.login()
        VisaRoleFactory(user=user)
        response = self.get(self.url()).json()

        self.assertEqual(len(response["globalRoles"]), 1)
        self.assertEqual(response["globalRoles"][0]["name"], "VisaRole")

    def test_control_roles(self):
        """
        Les rôles du contrôle sont serialisées dans le call du logged user
        """
        user = self.login()
        ControlRoleFactory(user=user)
        response = self.get(self.url()).json()

        self.assertEqual(len(response["globalRoles"]), 1)
        self.assertEqual(response["globalRoles"][0]["name"], "ControlRole")

    def test_mandated_companies(self):
        """
        Un·e utilisateur·ice doit voir les entreprises representées par son
        entreprise - et ce avec le même rôle de déclarant
        """
        company_1 = CompanyFactory()
        company_2 = CompanyFactory()

        user = self.login()

        # L'utilisateur·ice a un rôle déclaration dans company_1
        DeclarantRoleFactory(user=user, company=company_1)

        # company_2 mandate company_1 pour ses déclarations
        company_2.mandated_companies.add(company_1)
        company_2.save()

        response = self.get(self.url())
        companies = response.data["companies"]

        # L'utilisateur·ice doit donc avoir le droit de déclaration sur les deux entreprises
        self.assertEqual(len(companies), 2)
        self.assertEqual(len(list(filter(lambda x: x["id"] == company_1.id, companies))), 1)
        self.assertEqual(len(list(filter(lambda x: x["id"] == company_2.id, companies))), 1)


class TestCreateUser(ProjectAPITestCase):
    viewname = "user_create"

    def setUp(self):
        self.user_data = dict(
            last_name="Cook", first_name="Tim", email="tim.cook@example.com", username="tcook", password="azerty123$"
        )

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_create_user_ok(self, mocked_brevo):
        response = self.post(self.url(), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        new_user = User.objects.get(id=response.data["id"])
        self.assertEqual(new_user.email, self.user_data["email"])
        self.assertTrue(new_user.is_active)
        self.assertFalse(new_user.is_verified)
        self.assertFalse(new_user.is_superuser)
        self.assertFalse(new_user.is_staff)
        self.assertEqual(new_user.get_global_roles(), [])

        template_id = 19
        self.assertEqual(mocked_brevo.call_count, 1)
        self.assertEqual(mocked_brevo.call_args_list[0][0][0], template_id)
        self.assertEqual(mocked_brevo.call_args_list[0][0][2], new_user.email)
        self.assertEqual(mocked_brevo.call_args_list[0][0][3], new_user.get_full_name())

    def test_create_user_with_existing_email(self):
        email = "eren@example.com"
        UserFactory(email=email)
        self.user_data["email"] = email

        response = self.post(self.url(), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["field_errors"])

    def test_create_user_with_existing_username(self):
        username = "eren"
        UserFactory(username=username)
        self.user_data["username"] = username

        response = self.post(self.url(), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data["field_errors"])

    def test_create_user_with_invalid_password(self):
        self.user_data["password"] = "123"  # invalid
        response = self.post(self.url(), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["field_errors"])


class TestGetUser(ProjectAPITestCase):
    viewname = "user_retrieve_update_destroy"

    def setUp(self):
        self.user_data = dict(last_name="Cook", first_name="Tim", email="tim.cook@example.com", username="tcook")
        self.user = UserFactory(**self.user_data, is_verified=True)

    def test_get_user_as_instructor_ok(self):
        instructor_role = InstructionRoleFactory()
        self.login(instructor_role.user)
        response = self.get(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_as_logged_user_ok(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_not_authorized_ko(self):
        response = self.get(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestGetUserForController(ProjectAPITestCase):
    viewname = "retrieve_control_user"

    def setUp(self):
        self.user_data = dict(last_name="Cook", first_name="Tim", email="tim.cook@example.com", username="tcook")
        self.user = UserFactory(**self.user_data, is_verified=True)

    def test_get_user_as_controller_ok(self):
        instructor_role = ControlRoleFactory()
        self.login(instructor_role.user)
        response = self.get(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_not_authorized_ko(self):
        response = self.get(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestEditUser(ProjectAPITestCase):
    viewname = "user_retrieve_update_destroy"

    def setUp(self):
        self.user_data = dict(last_name="Cook", first_name="Tim", email="tim.cook@example.com", username="tcook")
        self.user = UserFactory(**self.user_data, is_verified=True)

    def test_edit_user_ok(self):
        self.login(self.user)
        new_last_name = "Cookie"
        response = self.put(self.url(pk=self.user.id), self.user_data | dict(last_name=new_last_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["last_name"], new_last_name)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, new_last_name)
        self.assertTrue(self.user.is_verified)  # user is still verified since email has not been changed

    def test_edit_user_with_email_changed_ok(self):
        self.login(self.user)
        new_email = "tim.cookie@example.com"
        response = self.put(self.url(pk=self.user.id), self.user_data | dict(email=new_email))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], new_email)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)
        self.assertFalse(self.user.is_verified)

    def test_edit_user_with_existing_email_ko(self):
        existing_email = "sundar.pichai@example.com"
        UserFactory(email=existing_email)
        self.login(self.user)
        response = self.put(self.url(pk=self.user.id), self.user_data | dict(email=existing_email))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["field_errors"])

    def test_edit_user_with_missing_data_ko(self):
        self.login(self.user)
        response = self.put(self.url(pk=self.user.id), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # NOTE: first_name and last_name are not mandatory at back-end level (should they?)
        self.assertEqual(len(response.data["field_errors"]), 2)

    def test_edit_user_other_than_me_ko(self):
        not_me = UserFactory()
        self.login(self.user)
        response = self.put(self.url(pk=not_me.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_user_unauthenticated(self):
        response = self.put(self.url(pk=self.user.id), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteUser(ProjectAPITestCase):
    viewname = "user_retrieve_update_destroy"

    def setUp(self):
        self.user = UserFactory(is_verified=True)

    def test_delete_user_ok(self):
        self.assertTrue(self.user.is_active)
        self.login(self.user)
        response = self.delete(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_delete_user_other_than_me_ko(self):
        not_me = UserFactory()
        self.login(self.user)
        response = self.delete(self.url(pk=not_me.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_unauthenticated(self):
        response = self.delete(self.url(pk=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestChangePassword(ProjectAPITestCase):
    viewname = "change_password"

    def setUp(self):
        self.password = "azerty123$"
        self.user = UserFactory(password=self.password)

    def test_change_password_ok(self):
        new_password = "azerty321$"
        self.login(self.user)
        response = self.post(
            self.url(), dict(old_password=self.password, new_password=new_password, confirm_new_password=new_password)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_with_invalid_old_password(self):
        new_password = "azerty321$"
        self.login(self.user)
        response = self.post(
            self.url(),
            dict(old_password="wrong-pasword", new_password=new_password, confirm_new_password=new_password),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data["field_errors"])

    def test_change_password_with_identical_new_password(self):
        self.login(self.user)
        response = self.post(
            self.url(),
            dict(old_password=self.password, new_password=self.password, confirm_new_password=self.password),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data["field_errors"])

    def test_change_password_with_invalid_new_password(self):
        new_password = "a"
        self.login(self.user)
        response = self.post(
            self.url(), dict(old_password=self.password, new_password=new_password, confirm_new_password=new_password)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["non_field_errors"])  # Django default behaviour

    def test_change_password_with_wrong_confirm(self):
        new_password = "azerty321$"
        self.login(self.user)
        response = self.post(
            self.url(),
            dict(old_password=self.password, new_password=new_password, confirm_new_password=new_password + "."),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_new_password", response.data["field_errors"])

    def test_change_password_unauthenticated(self):
        response = self.post(self.url(), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestGenerateUsername(ProjectAPITestCase):
    viewname = "generate_username"

    def test_generate_username(self):
        response = self.get(self.url() + "?first_name=jean&last_name=dupon")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"username": "jean.dupon"})

    def test_special_chars(self):
        response = self.get(self.url() + "?first_name=S.L.&last_name=UNIK%20HEALTH&NUTRITION")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"username": "sl.unik-health"})
