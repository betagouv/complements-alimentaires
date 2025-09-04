import logging

from django.db.models import Q

from data.models import Declaration, Snapshot

logger = logging.getLogger(__name__)

# Ce fichier contient des methodes utiles à calculer le statut simplifié, utilisé
# dans le contexte des contrôleurs.


class SimplifiedStatusHelper:
    MARKET_READY = "Commercialisation possible"
    ONGOING = "En cours d'instruction"
    REFUSED = "Commercialisation refusée"
    WITHDRAWN = "Retiré du marché"
    INTERRUPTED = "Instruction interrompue"

    @classmethod
    def get_passthrough_articles(cls):
        return (
            Declaration.Article.ARTICLE_15,
            Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION,
            Declaration.Article.ARTICLE_15_WARNING,
        )

    @classmethod
    def get_ongoing_instruction_statuses(cls):
        return (
            Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
            Declaration.DeclarationStatus.AWAITING_VISA,
            Declaration.DeclarationStatus.ONGOING_VISA,
            Declaration.DeclarationStatus.OBJECTION,
            Declaration.DeclarationStatus.OBSERVATION,
        )

    @classmethod
    def get_simplified_status(cls, declaration):
        if declaration.status == Declaration.DeclarationStatus.AUTHORIZED:
            return cls.MARKET_READY
        if declaration.status in cls.get_ongoing_instruction_statuses():
            return cls.MARKET_READY if declaration.article in cls.get_passthrough_articles() else cls.ONGOING
        if declaration.status == Declaration.DeclarationStatus.WITHDRAWN:
            return cls.WITHDRAWN
        if declaration.status == Declaration.DeclarationStatus.REJECTED:
            return cls.REFUSED
        if declaration.status == Declaration.DeclarationStatus.ABANDONED:
            return cls.INTERRUPTED
        return None

    @classmethod
    def get_filter_conditions(cls, simplified_status_values, query_prefix=""):
        """
        Retourne un objet Q utilisé pour filtrer les déclarations avec un des status simplifiés.
        Le query_prefix (optionnel) permet d'utiliser cet objet dans des relations, par exemple,
        si on fait le filtre depuis un objet Company, le query_prefix serait "declarations__"
        """
        conditions = Q()
        passthrough_articles = cls.get_passthrough_articles()
        ongoing_instruction = cls.get_ongoing_instruction_statuses()

        status_key = query_prefix + "status"
        status_in_key = query_prefix + "status__in"
        article_in_key = query_prefix + "article__in"

        for status_value in simplified_status_values:
            if status_value == cls.MARKET_READY:
                conditions |= Q(
                    Q(**{status_key: Declaration.DeclarationStatus.AUTHORIZED})
                    | Q(**{status_in_key: ongoing_instruction, article_in_key: passthrough_articles})
                )
            elif status_value == cls.ONGOING:
                conditions |= Q(**{status_in_key: ongoing_instruction}) & ~Q(**{article_in_key: passthrough_articles})
            elif status_value == cls.REFUSED:
                conditions |= Q(**{status_in_key: Declaration.DeclarationStatus.REJECTED})
            elif status_value == cls.WITHDRAWN:
                conditions |= Q(**{status_in_key: Declaration.DeclarationStatus.WITHDRAWN})
            elif status_value == cls.INTERRUPTED:
                conditions |= Q(**{status_in_key: Declaration.DeclarationStatus.ABANDONED})

        return conditions

    @classmethod
    def get_simplified_status_date(cls, instance):
        """
        La date qui nous intéresse peut concerner des snapshots différents
        """
        snapshots = instance.snapshots
        passthrough_articles = cls.get_passthrough_articles()
        ongoing_instruction = cls.get_ongoing_instruction_statuses()
        queryset = None
        if instance.status == Declaration.DeclarationStatus.AUTHORIZED:
            if instance.article in passthrough_articles:
                queryset = snapshots.filter(action=Snapshot.SnapshotActions.SUBMIT)
            else:
                queryset = snapshots.filter(status=Declaration.DeclarationStatus.AUTHORIZED)
        elif instance.status in ongoing_instruction:
            queryset = snapshots.filter(action=Snapshot.SnapshotActions.SUBMIT)
        elif instance.status == Declaration.DeclarationStatus.WITHDRAWN:
            queryset = snapshots.filter(action=Snapshot.SnapshotActions.WITHDRAW)
        elif instance.status == Declaration.DeclarationStatus.REJECTED:
            queryset = snapshots.filter(status=Declaration.DeclarationStatus.REJECTED)
        elif instance.status == Declaration.DeclarationStatus.ABANDONED:
            queryset = snapshots.filter(action=Snapshot.SnapshotActions.ABANDON)
        else:
            return None

        return queryset.latest("creation_date").creation_date if queryset.exists() else None
