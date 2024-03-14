# https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

import logging
from typing import Literal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ProjectAPIException(APIException):
    """
    Raise for specific exceptions related to this project.
    Additional binded data will be injected in the error response
    to allow front-end to deal with the exception.

    Parameters:
    * display: to know how to display the error:
        - 'global' -> in a toast
        - 'non_field' -> at the top of the form
        - 'field' -> on a specific field
    * field_name: if display is 'field', provide the field name
    * log_level: allow to provide the log level of the exception

    Note that every exception can be overrided when instanciated. This can be handful to adapt the error the context.
    """

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        display: Literal["global", "non_field", "field"] = None,
        field_name: str | None = None,
        log_level: str | None = logging.INFO,
        **detail_values: str,  # optionnaly inject dynamic values in error messages
    ):
        super().__init__()

        if self.__class__.__subclasses__():
            raise NotImplementedError(f"{self.__class__.__name__} should not be instanciated directly.")

        # Define attributes from class definition or object instanciation
        for attr_name, attr_value in {
            "display": display,
            "field_name": field_name,
        }.items():
            if attr_value:
                setattr(self, attr_name, attr_value)
            elif hasattr(self.__class__, attr_name):
                setattr(self, attr_name, getattr(self.__class__, attr_name))

        # Verification Checks
        if not self.detail or not self.display:
            raise ValueError(
                "A 'detail' and an 'display' must be defined, either in class definition, either in object instanciation."
            )

        if bool(self.display == "field") != hasattr(self, "field_name"):
            raise ValueError("'field_name' must be defined when display is 'field'")

        # Inject dynamic values
        self.detail = self.detail.format(**detail_values)

        # Create a log (not not) using provided log level
        if log_level:
            logger.log(level=log_level, msg=self.detail)


def custom_exception_handler(exc, context):
    """This will be called as soon as any exception occured in a DRF endpoint"""

    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    if response:  # exc is instance of DRF APIException (or Django Http404 / PermissionDenied)
        if isinstance(exc, ProjectAPIException):
            response.data |= exc.__dict__
        else:
            response.data |= {"display": "global"}
    else:  # Other uncaugh error that should not be displayed to the client
        new_exc = APIException()  # we'll show this chosen error to the client instead
        response = Response(
            data={"display": "global"} | new_exc.__dict__,
            status=new_exc.status_code,
        )

    return response
