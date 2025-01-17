import contextlib
import logging
import re
from datetime import date, datetime, timezone

from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.db import IntegrityError

from phonenumber_field.phonenumber import PhoneNumber

from data.models import GalenicFormulation, SubstanceUnit
from data.models.company import ActivityChoices, Company
from data.models.declaration import Declaration
from data.models.teleicare_history.ica_declaration import (
    IcaComplementAlimentaire,
    IcaDeclaration,
    IcaVersionDeclaration,
)
from data.models.teleicare_history.ica_etablissement import IcaEtablissement

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def suppress_autotime(model, fields):
    """
    Décorateur pour annuler temporairement le auto_now et auto_now_add de certains champs
    Copié depuis https://stackoverflow.com/questions/7499767/temporarily-disable-auto-now-auto-now-add
    """
    _original_values = {}
    for field in model._meta.local_fields:
        if field.name in fields:
            _original_values[field.name] = {
                "auto_now": field.auto_now,
                "auto_now_add": field.auto_now_add,
            }
            field.auto_now = False
            field.auto_now_add = False
    try:
        yield
    finally:
        for field in model._meta.local_fields:
            if field.name in fields:
                field.auto_now = _original_values[field.name]["auto_now"]
                field.auto_now_add = _original_values[field.name]["auto_now_add"]


def convert_phone_number(phone_number_to_parse):
    if phone_number_to_parse:
        phone_number = PhoneNumber.from_string(phone_number_to_parse, region="FR")
        return phone_number
    return ""


def convert_activities(etab):
    activities = []
    if etab.etab_ica_faconnier:
        activities.append(ActivityChoices.FAÇONNIER)
    if etab.etab_ica_fabricant:
        activities.append(ActivityChoices.FABRICANT)
    if etab.etab_ica_importateur:
        activities.append(ActivityChoices.IMPORTATEUR)
    if etab.etab_ica_introducteur:
        activities.append(ActivityChoices.INTRODUCTEUR)
    if etab.etab_ica_conseil:
        activities.append(ActivityChoices.CONSEIL)
    if etab.etab_ica_distributeur:
        activities.append(ActivityChoices.DISTRIBUTEUR)

    return activities


def match_companies_on_siret_or_vat(create_if_not_exist=False):
    """
    Le matching pourrait aussi être fait sur
    * Q(social_name__icontains=etab.etab_raison_sociale)
    * Q(commercial_name__icontains=etab.etab_enseigne)
    * Q(email__icontains=etab.etab_courriel)
    * Q(phone_number__icontains=etab.etab_telephone)
    Mais il serait moins précis.
    Cette méthode créé les entreprises non matchées pour avoir toutes les données intégrées dans le nouveau système.
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
                    matched = True
                    siret_matching[0].siccrf_id = etab.etab_ident
                    siret_matching[0].matched = True
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
                    matched = True
                    vat_matching[0].siccrf_id = etab.etab_ident
                    vat_matching[0].matched = True
                    vat_matching[0].save()
        # creation de la company
        if not matched and create_if_not_exist:
            new_company = Company(
                siccrf_id=etab.etab_ident,
                address=etab.etab_adre_voie,
                postal_code=etab.etab_adre_cp,
                city=etab.etab_adre_ville,
                phone_number=convert_phone_number(etab.etab_telephone),
                email=etab.etab_courriel or "",
                social_name=etab.etab_raison_sociale,
                commercial_name=etab.etab_enseigne or "",
                siret=etab.etab_siret,
                vat=etab.etab_numero_tva_intra,
                activities=convert_activities(etab),
                # la etab_date_adhesion n'est pas conservée
            )
            try:
                new_company.save(fields_with_no_validation=("phone_number"))
                nb_created_companies += 1
            except ValidationError as e:
                logger.error(f"Impossible de créer la Company à partir du siccrf_id = {etab.etab_ident}: {e}")

    logger.info(
        f"Sur {len(IcaEtablissement.objects.all())} : {nb_siret_match} entreprises réconcilliées par le siret."
    )
    logger.info(
        f"Sur {len(IcaEtablissement.objects.all())} : {nb_vat_match} entreprises réconcilliées par le n°TVA intracom."
    )
    logger.info(f"Sur {len(IcaEtablissement.objects.all())} : {nb_created_companies} entreprises créées.")


def get_most_recent(list_of_declarations):
    most_recent_date = date.min
    for ica_declaration in list_of_declarations:
        current_date = convert_str_date(ica_declaration.dcl_date)
        if most_recent_date < current_date:
            most_recent_date = current_date
            most_recent_dcl_date = ica_declaration.dcl_date

    return list_of_declarations.get(dcl_date=most_recent_dcl_date)


def convert_str_date(value, aware=False):
    dt = datetime.strptime(value, "%m/%d/%Y %H:%M:%S %p")
    if aware:
        return dt.replace(tzinfo=timezone.utc)
    else:
        return dt.date()


# Pour les déclarations TeleIcare, le status correspond au champ IcaVersionDeclaration.stattdcl_ident
DECLARATION_STATUS_MAPPING = {
    1: Declaration.DeclarationStatus.ONGOING_INSTRUCTION,  # 'en cours'
    2: Declaration.DeclarationStatus.AUTHORIZED,  # 'autorisé temporaire'
    3: Declaration.DeclarationStatus.AUTHORIZED,  # 'autorisé prolongé'  aucune occurence
    4: Declaration.DeclarationStatus.AUTHORIZED,  # 'autorisé définitif'  aucune occurence
    5: Declaration.DeclarationStatus.REJECTED,  # 'refusé'
    6: Declaration.DeclarationStatus.WITHDRAWN,  # 'arrêt commercialisation'
    7: Declaration.DeclarationStatus.WITHDRAWN,  # 'retiré du marché' aucune occurence
    8: Declaration.DeclarationStatus.ABANDONED,  # 'abandonné'
}


def create_declaration_from_teleicare_history():
    """
    Dans Teleicare une entreprise peut-être relié à une déclaration par 3 relations différentes :
    * responsable de l'étiquetage (équivalent Declaration.mandated_company)
    * gestionnaire de la déclaration (équivalent Declaration.company)
    * télédéclarante de la déclaration (cette relation n'est pour le moment pas conservée, car le BEPIAS ne sait pas ce qu'elle signifie)
    """
    nb_created_declarations = 0
    nb_missing_entp = 0

    for ica_complement_alimentaire in IcaComplementAlimentaire.objects.all():
        try:
            company = Company.objects.get(siccrf_id=ica_complement_alimentaire.etab_id)
        except Company.DoesNotExist:
            nb_missing_entp += 1
            continue
        # retrouve la déclaration la plus à jour correspondant à ce complément alimentaire
        all_ica_declarations = IcaDeclaration.objects.filter(cplalim_id=ica_complement_alimentaire.cplalim_ident)
        # le champ date est stocké en text, il faut donc faire la conversion en python
        if all_ica_declarations.exists():
            try:
                latest_ica_declaration = get_most_recent(all_ica_declarations)
            except MultipleObjectsReturned:
                logger.error(
                    f"Ce IcaComplementAlimentaire cplalim_ident={ica_complement_alimentaire.cplalim_ident} n'a pas une unique déclaration la plus récente"
                )
                continue
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
            # la déclaration a une version finalisée
            if latest_ica_version_declaration:
                declaration_creation_date = (
                    convert_str_date(latest_ica_declaration.dcl_date, aware=True)
                    if latest_ica_declaration.dcl_date
                    else ""
                )
                unit_quantity = re.findall(r"\d+", latest_ica_version_declaration.vrsdecl_djr)
                declaration = Declaration(
                    creation_date=declaration_creation_date,
                    modification_date=convert_str_date(
                        latest_ica_declaration.dcl_date_fin_commercialisation, aware=True
                    )
                    if latest_ica_declaration.dcl_date_fin_commercialisation
                    else declaration_creation_date,
                    siccrf_id=ica_complement_alimentaire.cplalim_ident,
                    galenic_formulation=GalenicFormulation.objects.get(
                        siccrf_id=ica_complement_alimentaire.frmgal_ident
                    ),
                    company=company,  # resp étiquetage, resp commercialisation
                    brand=ica_complement_alimentaire.cplalim_marque or "",
                    gamme=ica_complement_alimentaire.cplalim_gamme or "",
                    name=ica_complement_alimentaire.cplalim_nom,
                    flavor=ica_complement_alimentaire.dclencours_gout_arome_parfum or "",
                    other_galenic_formulation=ica_complement_alimentaire.cplalim_forme_galenique_autre or "",
                    # extraction d'un nombre depuis une chaîne de caractères
                    unit_quantity=unit_quantity[0] if unit_quantity else None,
                    unit_measurement=SubstanceUnit.objects.get(siccrf_id=latest_ica_version_declaration.unt_ident),
                    conditioning=latest_ica_version_declaration.vrsdecl_conditionnement or "",
                    daily_recommended_dose=latest_ica_version_declaration.vrsdecl_poids_uc,
                    minimum_duration=latest_ica_version_declaration.vrsdecl_durabilite,
                    instructions=latest_ica_version_declaration.vrsdecl_mode_emploi or "",
                    warning=latest_ica_version_declaration.vrsdecl_mise_en_garde or "",
                    # TODO: ces champs proviennent de tables pas encore importées
                    # populations=
                    # conditions_not_recommended=
                    # other_conditions=
                    # effects=
                    # other_effects=
                    # address=
                    # postal_code=
                    # city=
                    # country=
                    status=Declaration.DeclarationStatus.WITHDRAWN
                    if latest_ica_declaration.dcl_date_fin_commercialisation
                    else DECLARATION_STATUS_MAPPING[latest_ica_version_declaration.stattdcl_ident],
                )

                try:
                    with suppress_autotime(declaration, ["creation_date", "modification_date"]):
                        declaration.save()
                        nb_created_declarations += 1
                except IntegrityError:
                    # cette Déclaration a déjà été créée
                    pass

    logger.info(f"Sur {len(IcaComplementAlimentaire.objects.all())} : {nb_created_declarations} déclarations créées.")
    logger.info(f"{nb_missing_entp} entreprises à créer.")
