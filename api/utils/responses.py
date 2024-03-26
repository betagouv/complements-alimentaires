from rest_framework.response import Response
from rest_framework import status

EmptyValidResponse = Response({}, status=status.HTTP_200_OK)
