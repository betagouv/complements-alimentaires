import logging

from data.models import Company, IcaEtablissement, IcaVersionDeclaration
from data.models.declaration import Declaration, DeclarationStatus

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
            # seulement 2 options possible pour len(siret_matching) sont 0 et 1 car il y a une contrainte d'unicité sur le champ Company.siret
            if len(siret_matching) == 1:
                if siret_matching[0].siccrf_id is not None and etab.etab_ident != siret_matching[0].siccrf_id:
                    logger.error(
                        "Plusieurs Etablissement provenant de Teleicare ont le même SIRET, ce qui rend le matching avec une Company Compl'Alim incertain."
                    )
                else:
                    nb_siret_match += 1
                    siret_matching[0].siccrf_id = etab.etab_ident
                    siret_matching[0].save()

        elif etab.etab_numero_tva_intra is not None:
            vat_matching = Company.objects.filter(vat=etab.etab_numero_tva_intra)
            # seulement 2 options possible pour len(vat_matching) sont 0 et 1 car il y a une contrainte d'unicité sur le champ Company.vat
            if len(vat_matching) == 1:
                if vat_matching[0].siccrf_id is not None and etab.etab_ident != vat_matching[0].siccrf_id:
                    logger.error(
                        "Plusieurs Etablissement provenant de Teleicare ont le même n° TVA, ce qui rend le matching avec une Company Compl'Alim incertain."
                    )
                else:
                    nb_vat_match += 1
                    vat_matching[0].siccrf_id = etab.etab_ident
                    vat_matching[0].save()

    logger.info(
        f"{nb_vat_match} + {nb_siret_match} entreprises réconcilliées sur {len(IcaEtablissement.objects.all())}"
    )


def create_declaration_from_teleicare_history():
    for company in Company.objects.exclude(siccrf_id=None):
        declared_food_supplements = IcaVersionDeclaration.object.filter(
            etab_ident=company.siccrf_id, stattdcl_ident_in=[]
        )
        len(declared_food_supplements)
        declaration = Declaration()
        declaration.save()


# Pout les déclarations TeleIcare, le status correspond au champ IcaVersionDeclaration.stattdcl_ident
DECLARATION_STATUS_MAPPING = {
    1: DeclarationStatus.ONGOING_INSTRUCTION,  # 'en cours'
    2: DeclarationStatus.AUTHORIZED,  # 'autorisé temporaire'
    3: DeclarationStatus.AUTHORIZED,  # 'autorisé prolongé'
    4: DeclarationStatus.AUTHORIZED,  # 'autorisé définitif'
    5: DeclarationStatus.REJECTED,  # 'refusé'
    6: DeclarationStatus.WITHDRAWN,  # 'arrêt commercialisation'
    7: DeclarationStatus.WITHDRAWN,  # 'retiré du marché'
    8: DeclarationStatus.ABANDONED,  # 'abandonné'
}
