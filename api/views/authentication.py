from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # will create the user session
            return Response({"csrf_token": get_token(request)})
        else:
            # TODO: change with back-end error (when merge will be done)
            return Response(status=400)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response()
