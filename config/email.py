from django.conf import settings

import sib_api_v3_sdk

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
api_client = sib_api_v3_sdk.ApiClient(configuration)
email_api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)


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
