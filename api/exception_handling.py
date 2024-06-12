# https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class ProjectAPIException(Exception):
    """
    This is the base Exception used to create any DRF error. It is used in two ways:
    1) by custom DRF handler, to format response accordingly
    2) by ourselves, subclassing and raising this exception in our views.

    Parameters:
    * global_error: error to be displayed globally (e.g. in a toast)
    * non_field_errors: errors to be displayed at a top of a form
    * field_errors: errors to be displayed on a specific form field
    * log_level: allow to provide the log level of the exception

    Example of __dict__ value:
    {
        "global_error": "msg",
        "non_field_errors": ["msg", "msg"],
        "field_errors": {"field_1": ["msg", "msg"], "field_2": ["msg"]}
    }


    Note that every exception can be overrided when instanciated. This can be handful to adapt the error the context.
    """

    def __init__(
        self,
        global_error: str | None = None,
        non_field_errors: list[str] | None = None,
        field_errors: dict[str, list[str]] | None = None,
        log_level: int | None = logging.INFO,
        extra: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Define attributes from class definition or object instanciation
        for attr_name, (attr_value, default_type) in {
            "global_error": (global_error, None),
            "non_field_errors": (non_field_errors, list),
            "field_errors": (field_errors, dict),
        }.items():
            if attr_value:
                setattr(self, attr_name, attr_value)
            elif hasattr(self.__class__, attr_name):
                setattr(self, attr_name, getattr(self.__class__, attr_name))
            else:
                type_instance = default_type() if default_type else None
                setattr(self, attr_name, type_instance)

        # Verification Checks
        if not any([self.global_error, self.non_field_errors, self.field_errors]):
            raise ValueError("An exception must contain at least one error type.")

        # Inject addtional data of your choice into the response
        if extra:
            self.extra = extra

        # Create an optional log using provided log level
        if log_level:
            logger.log(level=log_level, msg=self.__class__.__name__, extra=self.__dict__)


def custom_exception_handler(exc, context):
    """This will be called as soon as any exception occured in a DRF endpoint"""

    response = exception_handler(exc, context)  # call DRF's default exception handler first
    if response:
        # CASE: DRF Validation error (e.g raised in serializer with `is_valid(raise_exception=True)`)
        if isinstance(exc, ValidationError):
            non_field_errors = response.data.pop(
                "non_field_errors", []
            )  # the base response should now contain only field errors
            response.data = ProjectAPIException(non_field_errors=non_field_errors, field_errors=response.data).__dict__
        # CASE: Other DRF APIException (or Django Http404 / PermissionDenied)
        else:
            response.data = ProjectAPIException(global_error=response.data["detail"]).__dict__
            # NOTE: status code is already set in the base response coming from the base `exception_handler`
    else:
        # CASE: ProjectAPIException raised directly from a view (already well formatted)
        if isinstance(exc, ProjectAPIException):
            response = Response(data=exc.__dict__, status=status.HTTP_400_BAD_REQUEST)
        # CASE: # Other uncaught error that should not be displayed to the client
        else:
            return None

    return response
