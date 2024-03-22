from urllib.parse import urljoin
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from api.serializers import LoggedUserSerializer, UserInputSerializer
from api.exception_handling import ProjectAPIException
from django.contrib.auth import get_user_model
from tokens.models import MagicLinkToken, MagicLinkUsage
from ..utils.urls import get_base_url

User = get_user_model()


class LoggedUserView(RetrieveAPIView):
    model = User
    serializer_class = LoggedUserSerializer
    queryset = get_user_model().objects.active()

    def get(self, request, *args, **kwargs):
        if permissions.IsAuthenticated().has_permission(self.request, self):
            return super().get(request, *args, **kwargs)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            new_token = MagicLinkToken.objects.create(user=new_user, usage=MagicLinkUsage.VERIFY_EMAIL_ADDRESS)
            verification_url = urljoin(get_base_url(request), new_token.as_url(key=new_token.key))
            send_mail(
                subject="Vérifiez votre adresse e-mail",
                message=f"Cliquez sur le lien suivant pour vérifier votre adresse e-mail : {verification_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
            )
            return Response({}, status=status.HTTP_201_CREATED)


class GenerateUsernameView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"username": User.generate_username(**request.query_params)})


class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        user = MagicLinkToken.run_email_verification(request.data["key"])
        if user:
            return Response({}, status=status.HTTP_200_OK)
        else:
            raise ProjectAPIException(
                global_error="Le lien de validation n'a pas fonctionné. Il a peut-être été déjà utilisé ou n'est plus valide."
            )
