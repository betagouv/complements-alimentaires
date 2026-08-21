from .celery import app
from celery import Task
import enum
from django.conf import settings

import sib_api_v3_sdk

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
api_client = sib_api_v3_sdk.ApiClient(configuration)
email_api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

HALF_DAY = 60 * 60 * 12


class EmailTaskWithRetry(Task):
    autoretry_for = (sib_api_v3_sdk.rest.ApiException,)
    max_retries = 5
    # reessayer : demie journée, un jour, deux jours, quatre jours, huit jours.
    # alors on a 15 jours pour resoudre le problème.
    retry_backoff = HALF_DAY
    retry_backoff_max = HALF_DAY * 32
    retry_jitter = False


class EmailTemplateID(enum.Enum):
    USER_ADDED_TO_COMPANY = 18
    CONFIRM_EMAIL = 19
    REQUEST_TO_JOIN_EMPTY_COMPANY = 15
    REQUEST_TO_JOIN_COMPANY = 12
    ACCEPT_REQUEST_TO_JOIN_COMPANY = 13
    REFUSE_REQUEST_TO_JOIN_COMPANY = 14
    INVITE_TO_JOIN_COMPANY = 16
    COMPANY_INVITATION_ACCEPTED = 17
    COMPANY_GIVEN_MANDATE = 27
    # Declaration flow
    DECLARATION_SUBMISSION_CONFIRMATION = 3
    DECLARATION_OBSERVATION = 4
    DECLARATION_OBJECTION = 5
    DECLARATION_AUTHORIZED = 6
    DECLARATION_WITHDRAWN = 8
    DECLARATION_AUTHORIZATION_REVOKED = 37
    DECLARATION_REJECTED = 7
    DECLARATION_EXPIRATION_REMINDER = 10
    DECLARATION_EXPIRED = 9


@app.task(base=EmailTaskWithRetry)
def send_sib_template(template_id, parameters, to_email, to_name):
    """
    Permet d'envoyer un email transactionnel précédemment défini dans Brevo.
    """
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        params=parameters,
        sender={"email": settings.CONTACT_EMAIL, "name": "Compl'Alim"},
        reply_to={"email": settings.CONTACT_EMAIL, "name": "Compl'Alim"},
        template_id=template_id,
    )
    email_api_instance.send_transac_email(send_smtp_email)
