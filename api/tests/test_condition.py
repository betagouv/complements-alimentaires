from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import ConditionFactory


class TestConditionApi(APITestCase):
    def test_get_condition_list(self):
        """
        The API should return all non obsolete conditions that are not missing data
        """
        complete_conditions = [ConditionFactory.create(missing_import_data=False, is_obsolete=False) for i in range(3)]
        incomplete_conditions = [
            ConditionFactory.create(missing_import_data=True, is_obsolete=False) for i in range(2)
        ]
        obsolete_conditions = [ConditionFactory.create(missing_import_data=True, is_obsolete=True) for i in range(3)]
        response = self.client.get(reverse("api:condition_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for condition in complete_conditions:
            self.assertTrue(any(x["id"] == condition.id for x in body))

        for condition in incomplete_conditions:
            self.assertFalse(any(x["id"] == condition.id for x in body))

        for condition in obsolete_conditions:
            self.assertFalse(any(x["id"] == condition.id for x in body))
