from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from api.serializers import LoggedUserSerializer, UserInputSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LoggedUserView(RetrieveAPIView):
    model = User
    serializer_class = LoggedUserSerializer
    queryset = get_user_model().objects.active()

    def get(self, request, *args, **kwargs):
        if permissions.IsAuthenticated().has_permission(self.request, self):
            return super().get(request, *args, **kwargs)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED)
