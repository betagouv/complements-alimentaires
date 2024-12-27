import logging

from data.models import Company, GalenicFormulation
from data.models.declaration import Declaration, DeclarationStatus
from data.models.teleicare_history import IcaComplementAlimentaire, IcaEtablissement

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
    """
    Dans Teleicare une entreprise peut-être relié à une déclaration par 3 relations différentes :
    * responsable de l'étiquetage (équivalent Declaration.mandated_company)
    * gestionnaire de la déclaration (équivalent Declaration.company)
    * télédéclarante de la déclaration (cette relation n'est pour le moment pas conservée, car le BEPIAS ne sait pas ce qu'elle signifie)
    """
    for ica_complement_alimentaire in IcaComplementAlimentaire.objects.all():
        declaration = Declaration(
            siccrf_id=ica_complement_alimentaire.cplalim_ident,
            galenic_formulation=GalenicFormulation.objects.filter(siccrf_id=ica_complement_alimentaire.frmgal_ident),
            company=ica_complement_alimentaire.etab_id,  # resp étiquetage, resp commercialisation
            brand=ica_complement_alimentaire.cplalim_marque,
            gamme=ica_complement_alimentaire.cplalim_gamme,
            name=ica_complement_alimentaire.cplalim_nom,
            flavor=ica_complement_alimentaire.dclencours_gout_arome_parfum,
            other_galenic_formulation=ica_complement_alimentaire.cplalim_forme_galenique_autre,
        )
        declaration.save()
        # for ica_declaration in IcaDeclaration.objects.filter(cplalim_ident=ica_complement_alimentaire.cplalim_ident).latest("dcl_date")
        # TODO : vérifier que la company existe déjà dans nos Company

        #  for company in Company.objects.exclude(siccrf_id=None):
        # # dans ce cas la company est responsable de l'étiquetage donc
        # declared_food_supplements = IcaComplementAlimentaire.object.filter(
        #     etab_ident=company.siccrf_id#, stattdcl_ident_in=[]
        # )
        # # dans ce cas la company est télédéclarante
        # declared_declaration = IcaVersionDeclaration.object.filter(
        #     etab_ident=company.siccrf_id,
        #     stadcl_ident=8, # état 'clos'
        #     stattdcl_ident_in=[2, 5, 6, 8], # status 'autorisé', 'refusé', 'arrêt commercialisation', 'abandonné'
        # )
        # # vérifie que l'entreprise "gestionnaire de la déclaration" selon TéléIcare est soit mandatée soit mandataire
        # declaration_managing_company_id = IcaDeclaration.objects.get().etab_iden
        # if declaration_managing_company !=
        #     logger.error("L'entreprise gestionnaire de la déclaration n'est ni l'entreprise mandataire ni l'entreprise mandatée.")


# Pout les déclarations TeleIcare, le status correspond au champ IcaVersionDeclaration.stattdcl_ident
DECLARATION_STATUS_MAPPING = {
    1: DeclarationStatus.ONGOING_INSTRUCTION,  # 'en cours'
    2: DeclarationStatus.AUTHORIZED,  # 'autorisé temporaire'
    3: DeclarationStatus.AUTHORIZED,  # 'autorisé prolongé'  aucune occurence
    4: DeclarationStatus.AUTHORIZED,  # 'autorisé définitif'  aucune occurence
    5: DeclarationStatus.REJECTED,  # 'refusé'
    6: DeclarationStatus.WITHDRAWN,  # 'arrêt commercialisation'
    7: DeclarationStatus.WITHDRAWN,  # 'retiré du marché' aucune occurence
    8: DeclarationStatus.ABANDONED,  # 'abandonné'
}
