from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import ConditionFactory


class TestConditionApi(APITestCase):
    def test_get_condition_list(self):
        """
        The API should return all non obsolete conditions that are not missing data
        """
        complete_conditions = [ConditionFactory.create(is_obsolete=False) for i in range(3)]
        obsolete_conditions = [ConditionFactory.create(is_obsolete=True) for i in range(3)]
        response = self.client.get(reverse("api:condition_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for condition in complete_conditions:
            self.assertTrue(any(x["id"] == condition.id for x in body))

        for condition in obsolete_conditions:
            self.assertFalse(any(x["id"] == condition.id for x in body))
