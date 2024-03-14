from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.views import APIView
from api.exception_handling import ProjectAPIException


class TestApiErrorMessages(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _build_response(self, endpoint):
        request = self.factory.get("/fake-url")
        view = endpoint.as_view()
        return view(request)

    def test_uncatchable_error(self):
        class Endpoint(APIView):
            def get(self, request):
                raise ValueError("This is a random error that should not be caught by the API")

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(str(response.data["detail"]), "A server error occurred.")
        self.assertEqual(str(response.data["display"]), "global")

    def test_project_error_with_global(self):
        class Error(ProjectAPIException):
            default_detail = "Message d'erreur"
            display = "global"

        class Endpoint(APIView):
            def get(self, request):
                raise Error

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Message d'erreur")
        self.assertEqual(response.data["display"], "global")
        self.assertNotIn("field_name", response.data)

    def test_project_error_with_field(self):
        class Error(ProjectAPIException):
            default_detail = "Message d'erreur"
            display = "field"
            field_name = "some_field"

        class Endpoint(APIView):
            def get(self, request):
                raise Error

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Message d'erreur")
        self.assertEqual(response.data["display"], "field")
        self.assertEqual(response.data["field_name"], "some_field")

    def test_drf_error(self):
        from rest_framework.exceptions import NotFound

        class Endpoint(APIView):
            def get(self, request):
                raise NotFound

        response = self._build_response(Endpoint)
        self.assertEqual(response.status_code, NotFound.status_code)
        self.assertEqual(str(response.data["detail"]), NotFound.default_detail)
        self.assertEqual(response.data["display"], "global")
        self.assertNotIn("field_name", response.data)
