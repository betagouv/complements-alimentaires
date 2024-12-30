import logging
import re

from data.models import Company, GalenicFormulation, SubstanceUnit
from data.models.declaration import Declaration, DeclarationStatus
from data.models.teleicare_history import (
    IcaComplementAlimentaire,
    IcaDeclaration,
    IcaEtablissement,
    IcaVersionDeclaration,
)

logger = logging.getLogger(__name__)


def match_or_create_companies_on_siret_or_vat():
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
    nb_created_companies = 0
    for etab in IcaEtablissement.objects.all():
        matched = False
        # recherche de l'etablissement dans les Company déjà enregistrées
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
        # retrouve la déclaration la plus à jour correspondant à ce complément alimentaire
        latest_ica_declaration = IcaDeclaration.objects.filter(
            cplalim_id=ica_complement_alimentaire.cplalim_ident, dcl_date_fin_commercialisation=None
        ).first()
        # le complément alimentaire est encore commercialisé
        if latest_ica_declaration:
            # retrouve la version de déclaration la plus à jour correspondant à cette déclaration
            latest_ica_version_declaration = IcaVersionDeclaration.objects.filter(
                dcl_id=latest_ica_declaration.dcl_ident,
                stattdcl_ident__in=[
                    2,
                    5,
                    6,
                    8,
                ],  # status 'autorisé', 'refusé', 'arrêt commercialisation', 'abandonné'
                stadcl_ident=8,  # état 'clos'
            ).first()
            # la déclaration à une version finalisée
            if latest_ica_version_declaration:
                try:
                    company = Company.objects.get(siccrf_id=ica_complement_alimentaire.etab_id)
                    declaration = Declaration(
                        siccrf_id=ica_complement_alimentaire.cplalim_ident,
                        galenic_formulation=GalenicFormulation.objects.get(
                            siccrf_id=ica_complement_alimentaire.frmgal_ident
                        ),
                        company=company,  # resp étiquetage, resp commercialisation
                        brand=ica_complement_alimentaire.cplalim_marque
                        if ica_complement_alimentaire.cplalim_marque
                        else "",
                        gamme=ica_complement_alimentaire.cplalim_gamme
                        if ica_complement_alimentaire.cplalim_gamme
                        else "",
                        name=ica_complement_alimentaire.cplalim_nom,
                        flavor=ica_complement_alimentaire.dclencours_gout_arome_parfum
                        if ica_complement_alimentaire.dclencours_gout_arome_parfum
                        else "",
                        other_galenic_formulation=ica_complement_alimentaire.cplalim_forme_galenique_autre
                        if ica_complement_alimentaire.cplalim_forme_galenique_autre
                        else "",
                        # extraction d'un nombre depuis une chaîne de caractères
                        unit_quantity=re.findall(r"\d+", latest_ica_version_declaration.vrsdecl_djr)[0],
                        unit_measurement=SubstanceUnit.objects.get(siccrf_id=latest_ica_version_declaration.unt_ident),
                        conditioning=latest_ica_version_declaration.vrsdecl_conditionnement
                        if latest_ica_version_declaration.vrsdecl_conditionnement
                        else "",
                        daily_recommended_dose=latest_ica_version_declaration.vrsdecl_poids_uc,
                        minimum_duration=latest_ica_version_declaration.vrsdecl_durabilite,
                        instructions=latest_ica_version_declaration.vrsdecl_mode_emploi
                        if latest_ica_version_declaration.vrsdecl_mode_emploi
                        else "",
                        warning=latest_ica_version_declaration.vrsdecl_mise_en_garde
                        if latest_ica_version_declaration.vrsdecl_mise_en_garde
                        else "",
                        # TODO: ces champs proviennent de tables pas encore importées
                        # populations=
                        # conditions_not_recommended=
                        # other_conditions=
                        # effects=
                        # other_effects=
                        # status=
                    )
                    declaration.save()
                except Company.DoesNotExist:
                    pass

        # else: # ajoute des déclaration dont la commercialisation est arrêtée


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
