import logging

from data.models import Company, IcaEtablissement

logger = logging.getLogger(__name__)


def match_companies_on_siret_or_vat():
    """
    Le matching pourrait aussi être fait sur
    * Q(social_name__icontains=etab.etab_raison_sociale)
    * Q(commercial_name__icontains=etab.etab_enseigne)
    * Q(email__icontains=etab.etab_courriel)
    * Q(phone_number__icontains=etab.etab_telephone)
    Mais il serait moins précis.
    """
    nb_vat_match = 0
    nb_siret_match = 0
    for etab in IcaEtablissement.objects.all():
        if etab.etab_siret is not None:
            siret_matching = Company.objects.filter(siret=etab.etab_siret)
            if len(siret_matching) == 1:
                nb_siret_match += 1
                siret_matching[0].siccrf_id = etab.etab_ident
                siret_matching[0].save()

        elif etab.etab_numero_tva_intra is not None:
            vat_matching = Company.objects.filter(vat=etab.etab_numero_tva_intra)
            if len(vat_matching) == 1:
                nb_vat_match += 1
                vat_matching[0].siccrf_id = etab.etab_ident
                vat_matching[0].save()

    logger.info(
        f"{nb_vat_match} + {nb_siret_match} entreprises réconcilliées sur {len(IcaEtablissement.objects.all())}"
    )
