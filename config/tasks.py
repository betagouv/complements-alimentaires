import logging
from datetime import datetime, time

from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, F, Max, Q
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from simple_history.utils import update_change_reason
from viewflow import fsm

from api.utils.simplified_status import SimplifiedStatusHelper
from config import email
from data.etl.transformer_loader import ETL_OPEN_DATA_DECLARATIONS
from data.models import Company, Declaration, Snapshot

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
    brevo_template_id = 9
    declarations = Declaration.objects.filter(status__in=allowed_statuses)

    success_count = 0
    error_count = 0
    early_count = 0
    logger.info(f"Starting the automatic expiration of {declarations.count()} declarations.")
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
            success_count += 1
        except EarlyExpirationError as _:
            early_count += 1
        except Exception as _:
            error_count += 1
            logger.exception(f"Could not expire declaration {declaration.id}")

    logger.info(f"{success_count} declarations were automatically expired.")
    logger.info(f"{early_count} declarations were not automatically expired, expiration_date has not passed.")
    if error_count:
        logger.error(f"{error_count} declarations failed automatic expiration.")


def send_automatic_validation_email(declaration):
    if not declaration.author:
        logger.log(f"Email not sent on automatic validation of declaration {declaration.id}: no author")
        return
    brevo_template_id = 6
    try:
        email.send_sib_template(
            brevo_template_id,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )
    except Exception as _:
        logger.exception(f"Email not sent on automatic validation of declaration {declaration.id}")


@app.task
def approve_declarations():
    if not settings.ENABLE_AUTO_VALIDATION:
        logger.info("Automatic validation of declarations disabled. Enable setting ENABLE_AUTO_VALIDATION.")
        return

    cutoff_delta = timezone.now() - relativedelta(days=14)

    declarations = (
        Declaration.objects
        # On prend seulement les déclatations en attente d'instruction et articles 15 / 15 vigilance population
        .filter(
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            article__in=[Declaration.Article.ARTICLE_15, Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION],
        )
        # Plus précisement, seulement les déclarations qui n'ont pas été traitées ni touchées par l'instruction,
        # et donc ont seulement des snapshots type "SUBMIT" (créés par le passage DRAFT => AWAITING_INSTRUCTION)
        .annotate(
            total_snapshot_count=Count("snapshots"),
            submit_snapshots_count=Count("snapshots", filter=Q(snapshots__action=Snapshot.SnapshotActions.SUBMIT)),
        )
        .filter(total_snapshot_count=F("submit_snapshots_count"))
        # Et finalement on ne prend que celles soumises au moins il y a deux mois
        .annotate(submission_date=Max("snapshots__creation_date"))
        .filter(submission_date__lt=cutoff_delta)
    )

    logger.info(f"Starting the automatic validation of {declarations.count()} declarations.")
    error_count = 0
    success_count = 0
    for declaration in declarations:
        try:
            declaration.status = Declaration.DeclarationStatus.AUTHORIZED
            with transaction.atomic():
                declaration.save()
                declaration.create_snapshot(action=Snapshot.SnapshotActions.AUTOMATICALLY_AUTHORIZE)
            success_count += 1
            send_automatic_validation_email(declaration)
        except Exception as _:
            logger.exception(f"Automatic validation of declaration {declaration.id} failed.")
            error_count += 1

    logger.info(f"{success_count} declarations were automatically validated.")
    if error_count:
        logger.error(f"{error_count} declarations failed automatic validation.")


@app.task
def export_datasets_to_data_gouv():
    etl = ETL_OPEN_DATA_DECLARATIONS()
    etl.extract_dataset()
    etl.transform_dataset()
    etl.load_dataset()


@app.task
def recalculate_article_for_ongoing_declarations(declarations, change_reason):
    for declaration in declarations.filter(
        status__in=(
            Declaration.DeclarationStatus.DRAFT,
            Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
            Declaration.DeclarationStatus.AWAITING_VISA,
            Declaration.DeclarationStatus.ONGOING_VISA,
            Declaration.DeclarationStatus.OBSERVATION,
            Declaration.DeclarationStatus.OBJECTION,
        ),
    ):
        previous_article = declaration.calculated_article
        declaration.assign_calculated_article()
        if previous_article != declaration.calculated_article:
            declaration.save()
            # il faut faire un refresh pour update_change_reason de retrouver le record à MAJ
            declaration.refresh_from_db()
            if len(change_reason) > 100:
                logger.warn(f"change_reason '{change_reason}' too long. Truncating to 100 characters.")
                change_reason = change_reason[:100]
            update_change_reason(declaration, change_reason)
            logger.info(f"Declaration {declaration.id} article recalculated.")


@app.task
def update_market_ready_counts():
    """
    Cette tâche met à jour le nombre de déclarations commecialisables pour les entreprises
    """
    logger.info("Starting the cache update for market-ready declarations")
    batch_size = 500
    market_ready_condition = SimplifiedStatusHelper.get_filter_conditions(
        [SimplifiedStatusHelper.MARKET_READY], "declarations__"
    )

    # Obtention de tous les IDs (requête rapide). Le triage par ID est important pour ne pas
    # avoir des résultats inconsistents dans la pagination.
    company_ids = Company.objects.order_by("id").values_list("id", flat=True)
    paginator = Paginator(company_ids, batch_size)

    for page_num in paginator.page_range:
        try:
            batch_ids = list(paginator.page(page_num).object_list)

            # Avec une seule requête on obtient les counts des declarations commercialisables
            companies_with_counts = Company.objects.filter(id__in=batch_ids).annotate(
                market_ready_count=Count("declarations", filter=market_ready_condition, distinct=True)
            )

            objects_to_save = []
            for company in companies_with_counts:
                company.market_ready_count_cache = company.market_ready_count
                company.market_ready_count_updated_at = timezone.now()
                objects_to_save.append(company)

            if not objects_to_save:
                continue
            Company.objects.bulk_update(objects_to_save, ["market_ready_count_cache", "market_ready_count_updated_at"])
            logger.info(f"Updated {len(objects_to_save)} companies ({page_num} of {paginator.page_range.stop - 1})")

        except Exception as e:
            logger.exception(e)

    logger.info("Cache update done!")
