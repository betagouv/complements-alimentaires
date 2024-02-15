from django.http import JsonResponse
from rest_framework import status

ERROR_FIELD = "error"

EmptyValidResponse = JsonResponse({}, status=status.HTTP_200_OK)
InvalidEmailResponse = JsonResponse({ERROR_FIELD: "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
UnknownErrorResponse = JsonResponse(
    {ERROR_FIELD: "An error has ocurred"},
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
)
