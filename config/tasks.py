import logging
from datetime import datetime, time

from django.utils import timezone

from viewflow import fsm

from config import email
from data.models import Declaration

from .celery import app

logger = logging.getLogger(__name__)
Status = Declaration.DeclarationStatus
allowed_statuses = [Status.OBJECTION, Status.OBSERVATION]


@app.task
def send_expiration_reminder():
    """
    Cette tâche ne doit être effectuée qu'une seule fois par jour, car elle s'appuie sur
    cette periodicité pour ne pas envoyer des doublons d'email
    """
    declarations = Declaration.objects.filter(status__in=allowed_statuses)
    brevo_template_id = 10
    send_days_before = 5
    for declaration in declarations:
        try:
            if not declaration.expiration_date:
                continue
            end_of_expiration_day = timezone.make_aware(datetime.combine(declaration.expiration_date, time.max))
            today = timezone.now()
            delta = end_of_expiration_day - today
            if delta.days >= send_days_before and delta.days < send_days_before + 1:
                parameters = {**declaration.brevo_parameters, **{"REMAINING_DAYS": send_days_before}}
                email.send_sib_template(
                    brevo_template_id,
                    parameters,
                    declaration.author.email,
                    declaration.author.get_full_name(),
                )

        except Exception as _:
            logger.exception(f"Could not send reminder email for declaration f{declaration.id}")


class EarlyExpirationError(Exception):
    pass


class ExpirationDeclarationFlow:
    status = fsm.State(Status, default=Status.DRAFT)

    def __init__(self, declaration):
        self.declaration = declaration

    @status.setter()
    def _set_declaration_state(self, value):
        self.declaration.status = value

    @status.getter()
    def _get_declaration_state(self):
        return self.declaration.status

    @status.on_success()
    def _on_transition_success(self, descriptor, source, target):
        self.declaration.save()

    @status.transition(source={Status.OBSERVATION, Status.OBJECTION}, target=Status.ABANDONED)
    def abandon(self):
        if self.declaration.snapshots.count() == 0:
            logger.warn(f"Declaration {self.declaration.id} cannot be expired because it has no snapshots")
            raise Exception()

        latest_snapshot = self.declaration.snapshots.latest("creation_date")
        if latest_snapshot.status not in allowed_statuses:
            logger.warn(
                f"Declaration {self.declaration.id} cannot be expired because its latest snapshot is not OBSERVATION or OBJECTION"
            )
            raise Exception()

        elif latest_snapshot.expiration_days is None or latest_snapshot.expiration_days == 0:
            logger.warn(
                f"Declaration {self.declaration.id} cannot be expired because its snapshot's expiration days is not correct"
            )
            raise Exception()

        today = timezone.now()
        if today < self.declaration.expiration_date:
            raise EarlyExpirationError()


@app.task
def expire_declarations():
    declarations = Declaration.objects.filter(status__in=allowed_statuses)
    brevo_template_id = 9
    for declaration in declarations:
        flow = ExpirationDeclarationFlow(declaration)
        try:
            flow.abandon()
            if declaration.author:
                email.send_sib_template(
                    brevo_template_id,
                    declaration.brevo_parameters,
                    declaration.author.email,
                    declaration.author.get_full_name(),
                )
        except EarlyExpirationError as _:
            break
        except Exception as _:
            logger.exception(f"Could not expire declaration f{declaration.id}")
