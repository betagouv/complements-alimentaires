from django.test import RequestFactory
from rest_framework import status
from rest_framework import serializers
from rest_framework.test import APITestCase
from rest_framework.views import APIView
from api.exception_handling import ProjectAPIException
from django.utils.translation import gettext_lazy as _


class TestProjectAPIException(APITestCase):
    def test_empty_error(self):
        with self.assertRaises(ValueError):
            ProjectAPIException()
        with self.assertRaises(ValueError):
            ProjectAPIException(global_error=None, non_field_errors=[], field_errors={})


class TestApiErrorMessages(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _build_response(self, endpoint, method="GET"):
        request = getattr(self.factory, method.lower())("/fake-url")
        view = endpoint.as_view()
        return view(request)

    def test_uncatchable_error(self):
        class Endpoint(APIView):
            def get(self, request):
                raise ValueError("This is a random error that should not be caught by the API")

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.data,
            {
                "global_error": "Une erreur innatendue est survenue, veuillez réessayer plus tard.",
                "non_field_errors": [],
                "field_errors": {},
            },
        )

    def test_project_error_with_global(self):
        class Error(ProjectAPIException):
            global_error = "Message d'erreur"

        class Endpoint(APIView):
            def get(self, request):
                raise Error

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"global_error": "Message d'erreur", "non_field_errors": [], "field_errors": {}}
        )

    def test_project_error_with_every_case(self):
        class Error(ProjectAPIException):
            field_errors = {"field_1": ["err1", "err2"], "field_2": ["err3"]}
            non_field_errors = ["err4", "err5"]
            global_error = "err6"

        class Endpoint(APIView):
            def get(self, request):
                raise Error

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "global_error": "err6",
                "non_field_errors": ["err4", "err5"],
                "field_errors": {"field_1": ["err1", "err2"], "field_2": ["err3"]},
            },
        )

    def test_drf_error(self):
        from rest_framework.exceptions import NotFound

        class Endpoint(APIView):
            def get(self, request):
                raise NotFound

        response = self._build_response(Endpoint)

        self.assertEqual(response.status_code, NotFound.status_code)
        self.assertEqual(response.data, {"global_error": _("Not found."), "non_field_errors": [], "field_errors": {}})

    def test_drf_validation_error_from_serializer(self):
        class Serializer(serializers.Serializer):
            important_field = serializers.CharField(required=True)

        class Endpoint(APIView):
            def post(self, request):
                serializer = Serializer(data={})
                serializer.is_valid(raise_exception=True)

        response = self._build_response(Endpoint, method="POST")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "global_error": None,
                "non_field_errors": [],
                "field_errors": {"important_field": ["Ce champ est obligatoire."]},
            },
        )
