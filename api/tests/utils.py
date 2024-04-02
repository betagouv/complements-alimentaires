import functools
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from data.factories import UserFactory
from rest_framework.test import APITestCase


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_func(*args, **kwargs):
        authenticate.user = UserFactory.create()
        args[0].client.force_login(user=authenticate.user)
        return func(*args, **kwargs)

    return authenticate_and_func


class ProjectAPITestCase(APITestCase):
    namespace = "api"
    viewname = None

    def url(self, *args, **kwargs):
        if not self.viewname:
            raise ImproperlyConfigured("Please provide a viewname attribute")
        return reverse(f"{self.namespace}:{self.viewname}", *args, **kwargs)

    def login(self, user=None):
        """Login the provided user, or a new one if not provided. Return the user"""

        if not user:
            user = UserFactory.create()
        self.client.force_login(user)
        return user

    # HTTP Method Sugar
    def get(self, url, *args, **kwargs):
        return self.client.get(url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.client.post(url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        return self.client.put(url, *args, **kwargs)

    def patch(self, url, *args, **kwargs):
        return self.client.patch(url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.client.delete(url, *args, **kwargs)
