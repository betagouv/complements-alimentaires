from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from api.serializers import LoggedUserSerializer
from django.contrib.auth import get_user_model


class LoggedUserView(RetrieveAPIView):
    model = get_user_model()
    serializer_class = LoggedUserSerializer
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        if permissions.IsAuthenticated().has_permission(self.request, self):
            return super().get(request, *args, **kwargs)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user
