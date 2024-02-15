from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def get_email_from_request(request, email_field="email", required=True) -> str | None:
    """Get an email from a request then normalize and validate it.
    If required == False, the email is tested only if it is provided.
    """

    raw_email = request.data.get(email_field)
    if not raw_email:
        if required:
            raise ValidationError("No email given")
        else:
            return None
    email = BaseUserManager.normalize_email(raw_email)
    validate_email(email)

    return email
