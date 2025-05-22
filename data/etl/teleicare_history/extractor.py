import logging
from datetime import date, datetime, timezone

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q

from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from data.behaviours.time_stampable import suppress_autotime
from data.models import (
    Condition,
    Effect,
    GalenicFormulation,
    Ingredient,
    Microorganism,
    Plant,
    PlantPart,
    Preparation,
    Snapshot,
    Substance,
    SubstanceUnit,
)
from data.models.company import ActivityChoices, Company, EtablissementToCompanyRelation
from data.models.declaration import (
    ComputedSubstance,
    Declaration,
    DeclaredIngredient,
    DeclaredMicroorganism,
    DeclaredPlant,
)
from data.models.teleicare_history.ica_declaration import (
    IcaComplementAlimentaire,
    IcaDeclaration,
    IcaEffetDeclare,
    IcaPopulationCibleDeclaree,
    IcaPopulationRisqueDeclaree,
    IcaVersionDeclaration,
)
from data.models.teleicare_history.ica_declaration_composition import (
    IcaIngredient,
    IcaIngredientAutre,
    IcaMicroOrganisme,
    IcaPreparation,
    IcaSubstanceDeclaree,
)
from data.models.teleicare_history.ica_etablissement import IcaEtablissement

logger = logging.getLogger(__name__)


def convert_phone_number(phone_number_to_parse):
    if phone_number_to_parse:
        try:
            phone_number = PhoneNumber.from_string(phone_number_to_parse, region="FR")
            return phone_number
        except NumberParseException:
            return ""
    return ""


def clean_vat(vat_to_parse):
    if vat_to_parse:
        return vat_to_parse.replace(" ", "").replace(".", "").replace("-", "")
    return None


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


def match_companies_on_siret_or_vat(create_if_not_exist=False, create_only_useful=True):
    """
    Le matching pourrait aussi être fait sur
    * Q(social_name__icontains=etab.etab_raison_sociale)
    * Q(commercial_name__icontains=etab.etab_enseigne)
    * Q(email__icontains=etab.etab_courriel)
    * Q(phone_number__icontains=etab.etab_telephone)
    Mais il serait moins précis.
    si create_if_not_exist=True, création des entreprises non matchées
    avec risque de doublon (si le SIRET/VAT avec lequel l'entreprise a été créée est différent)
    """
    nb_vat_match, nb_siret_match = 0, 0
    nb_creation_success, nb_creation_fail = 0, 0
    # ne créé que les etablissement qui ont des déclarations reliées
    if create_only_useful:
        used_etab_ident = (
            IcaComplementAlimentaire.objects.values_list("etab_id")
            .union(IcaDeclaration.objects.values_list("etab_id"))
            .union(IcaVersionDeclaration.objects.values_list("etab_id"))
        )
        etab_to_create = IcaEtablissement.objects.filter(etab_ident__in=used_etab_ident)
    else:
        etab_to_create = IcaEtablissement.objects.all()
    for etab in etab_to_create:
        matched = False
        # recherche de l'etablissement dans les Company déjà enregistrées
        if etab.etab_siret is not None:
            company_with_siret_matching = Company.objects.filter(
                Q(siret=etab.etab_siret) | Q(etablissementtocompanyrelation__old_siret=etab.etab_siret)
            )
            # seulement 2 options possible pour len(company_with_siret_matching) sont 0 et 1 car il y a une contrainte d'unicité sur le champ Company.siret
            if len(company_with_siret_matching) == 1:
                nb_siret_match += 1
                matched = True
                relation, _ = EtablissementToCompanyRelation.objects.get_or_create(
                    company=company_with_siret_matching[0],
                    old_siret=etab.etab_siret,
                )  # si le siret est celui actuel (Company.siret) la relation n'existe pas encore
                relation.siccrf_id = etab.etab_ident
                relation.siccrf_registration_date = convert_str_date(etab.etab_date_adhesion)
                try:
                    relation.save()
                except IntegrityError as err:
                    logger.error(f"Relation entre {relation.company_id} et {relation.siccrf_id} : {err}.")

        elif etab.etab_numero_tva_intra is not None:
            clean_numero_tva_intra = clean_vat(etab.etab_numero_tva_intra)
            company_with_vat_matching = Company.objects.filter(
                Q(vat=clean_numero_tva_intra) | Q(etablissementtocompanyrelation__old_vat=clean_numero_tva_intra)
            )
            # seulement 2 options possible pour len(company_with_vat_matching) sont 0 et 1 car il y a une contrainte d'unicité sur le champ Company.vat
            if len(company_with_vat_matching) == 1:
                nb_vat_match += 1
                matched = True
                relation, _ = EtablissementToCompanyRelation.objects.get_or_create(
                    company=company_with_vat_matching[0],
                    old_vat=clean_numero_tva_intra,
                )  # si le vat est celui actuel (Company.vat) la relation n'existe pas encore
                relation.siccrf_id = etab.etab_ident
                relation.siccrf_registration_date = convert_str_date(etab.etab_date_adhesion)
                try:
                    relation.save()
                except IntegrityError as err:
                    logger.error(f"Relation entre {relation.company_id} et {relation.siccrf_id} : {err}.")

        # creation de la company
        if not matched and create_if_not_exist:
            new_company = Company(
                address=etab.etab_adre_voie,
                postal_code=etab.etab_adre_cp,
                city=etab.etab_adre_ville,
                phone_number=convert_phone_number(etab.etab_telephone),
                email=etab.etab_courriel or "",
                social_name=etab.etab_raison_sociale,
                commercial_name=etab.etab_enseigne or "",
                siret=etab.etab_siret,
                vat=clean_vat(etab.etab_numero_tva_intra),
                activities=convert_activities(etab),
            )

            try:
                new_company.save(fields_with_no_validation=("phone_number"))
                relation = EtablissementToCompanyRelation(
                    company=new_company,
                    siccrf_id=etab.etab_ident,
                    old_siret=etab.etab_siret,
                    old_vat=clean_vat(etab.etab_numero_tva_intra),
                    siccrf_registration_date=convert_str_date(etab.etab_date_adhesion),
                )
                relation.save()
                nb_creation_success += 1
            except ValidationError as e:
                nb_creation_fail += 1
                logger.error(f"Impossible de créer la Company à partir du siccrf_id = {etab.etab_ident}: {e}")

    logger.info(f"Sur {etab_to_create.count()} : {nb_siret_match} entreprises réconcilliées par le siret.")
    logger.info(f"Sur {etab_to_create.count()} : {nb_vat_match} entreprises réconcilliées par le n°TVA intracom.")
    logger.info(
        f"Sur {etab_to_create.count()} : {nb_creation_success} entreprises créées, et {nb_creation_fail} non créées."
    )


def get_oldest_and_latest(list_of_declarations):
    """
    Cette fonction n'utilise pas les outils de comparaison de date de la BDD
    car le champ `dcl_date` est un champ text et non date
    """
    if len(list_of_declarations) == 1:
        return list_of_declarations[0], list_of_declarations[0]
    latest_date = date.min
    oldest_date = date.max
    for ica_declaration in list_of_declarations:
        current_date = convert_str_date(ica_declaration.dcl_date)
        if current_date > latest_date:
            latest_date = current_date
            latest_dcl_date = ica_declaration.dcl_date
        if current_date < oldest_date:
            oldest_date = current_date
            oldest_dcl_date = ica_declaration.dcl_date
    oldest = list_of_declarations.filter(dcl_date=oldest_dcl_date).order_by("dcl_numero").first()
    latest = list_of_declarations.filter(dcl_date=latest_dcl_date).order_by("dcl_numero").last()

    return oldest, latest


def convert_str_date(value, aware=False):
    if value is None:
        return
    dt = datetime.strptime(value, "%m/%d/%Y %H:%M:%S %p")
    if aware:
        return dt.replace(tzinfo=timezone.utc)
    else:
        return dt.date()


def create_teleicare_id(latest_ica_declaration):
    if latest_ica_declaration.dcl_annee and latest_ica_declaration.dcl_mois and latest_ica_declaration.dcl_numero:
        return "-".join(
            [
                str(getattr(latest_ica_declaration, field))
                for field in [
                    "dcl_annee",
                    "dcl_mois",
                    "dcl_numero",
                ]
            ]
        )


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

DECLARATION_TYPE_TO_ARTICLE_MAPPING = {
    1: Declaration.Article.ARTICLE_15,
    2: Declaration.Article.ARTICLE_16,
    3: None,  # Type "simplifié" dans Teleicare, normalement liées à des modifications de déclarations déjà instruites
}


def get_CA_corresponding_population(teleicare_population_ids):
    TARGET_POPULATION_MAPPING = {
        1: [6],  # Adolescents
        2: [],  # "Autre (à préciser)",
        3: [5],  # Enfants
        4: [4],  # Enfants en bas âge (1 à 3 ans)
        5: [12],  # Femmes
        6: [11],  # Hommes
        7: [10],  # Personnes agées
        9: [2, 3],  # Nourrissons (0 à 12 mois)
        10: [8],  # Femmes enceintes,
        11: [9],  # Femmes allaitantes
        # La population autre n'existe pas dans Compl'Alim
    }
    list_of_CA_population_id = []
    for teleicare_population_id in teleicare_population_ids:
        list_of_CA_population_id.extend(TARGET_POPULATION_MAPPING.get(teleicare_population_id, []))
    return list_of_CA_population_id


def compute_declaration_attributes(ica_complement_alimentaire, latest_ica_declaration, latest_ica_version_declaration):
    status = (
        Declaration.DeclarationStatus.WITHDRAWN
        if latest_ica_declaration.dcl_date_fin_commercialisation
        else DECLARATION_STATUS_MAPPING[latest_ica_version_declaration.stattdcl_ident]
    )
    mandated_company = None
    if latest_ica_declaration.etab_id is not None:
        try:
            # si l'entreprise mandataire a été créée sur Compl'Alim et matchée avec un Etablissement historique grâce au SIRET/VAT avec match_companies_on_siret_or_vat
            mandated_company = EtablissementToCompanyRelation.objects.get(
                siccrf_id=latest_ica_declaration.etab_id
            ).company
        except EtablissementToCompanyRelation.DoesNotExist:
            # ne devrait pas arriver si toutes les entreprises ont été créées avec match_companies_on_siret_or_vat(create_if_not_exist=True)
            logger.error(
                "La company mandataire etab_ident={latest_ica_declaration.etab_id} du complément alimentaire déclaré dans Teleicare cplalim_ident={ica_complement_alimentaire.cplalim_ident} n'existe pas dans Compl'Alim."
            )
    return {
        "mandated_company": mandated_company,
        "siccrf_id": ica_complement_alimentaire.cplalim_ident,
        "teleicare_id": create_teleicare_id(latest_ica_declaration),
        "galenic_formulation": GalenicFormulation.objects.get(siccrf_id=ica_complement_alimentaire.frmgal_ident),
        # resp étiquetage, resp commercialisation
        "brand": ica_complement_alimentaire.cplalim_marque or "",
        "gamme": ica_complement_alimentaire.cplalim_gamme or "",
        "name": ica_complement_alimentaire.cplalim_nom,
        "flavor": ica_complement_alimentaire.dclencours_gout_arome_parfum or "",
        "other_galenic_formulation": ica_complement_alimentaire.cplalim_forme_galenique_autre or "",
        # extraction d'un nombre depuis une chaîne de caractères
        "unit_quantity": latest_ica_version_declaration.vrsdecl_poids_uc,
        "unit_measurement": SubstanceUnit.objects.get(siccrf_id=latest_ica_version_declaration.unt_ident),
        "conditioning": latest_ica_version_declaration.vrsdecl_conditionnement or "",
        "daily_recommended_dose": latest_ica_version_declaration.vrsdecl_djr,
        "minimum_duration": latest_ica_version_declaration.vrsdecl_durabilite,
        "instructions": latest_ica_version_declaration.vrsdecl_mode_emploi or "",
        "warning": latest_ica_version_declaration.vrsdecl_mise_en_garde or "",
        "calculated_article": DECLARATION_TYPE_TO_ARTICLE_MAPPING[latest_ica_declaration.tydcl_ident],
        "status": status,
        # addresse responsable d'etiquetage
        "address": latest_ica_version_declaration.vrsdecl_adre_voie,
        "additional_details": latest_ica_version_declaration.vrsdecl_adre_comp or "",
        "postal_code": latest_ica_version_declaration.vrsdecl_adre_cp[
            :10
        ],  # from TextField to CharField(max_length=10)
        "city": latest_ica_version_declaration.vrsdecl_adre_ville,
        # "cedex": parfois compris dans vrsdecl_adre_comp ou vrsdecl_adre_comp2
        # "country":
    }


def create_declared_plant(declaration, teleIcare_plant, active):
    try:
        declared_plant = DeclaredPlant(
            declaration=declaration,
            plant=Plant.objects.get(siccrf_id=teleIcare_plant.plte_ident),
            active=active,
            quantity=teleIcare_plant.prepa_qte if active else None,
            unit=SubstanceUnit.objects.get(siccrf_id=teleIcare_plant.unt_ident) if active else None,
            preparation=Preparation.objects.get(siccrf_id=teleIcare_plant.typprep_ident) if active else None,
            used_part=PlantPart.objects.get(siccrf_id=teleIcare_plant.pplan_ident) if active else None,
        )
        return declared_plant
    except Plant.DoesNotExist as e:
        logger.error(e)
        return


def create_declared_microorganism(declaration, teleIcare_microorganism, active):
    try:
        declared_microorganism = DeclaredMicroorganism(
            declaration=declaration,
            microorganism=Microorganism.objects.get(siccrf_id=teleIcare_microorganism.morg_ident),
            active=active,
            activated=True,  # dans TeleIcare, le champ `activated` n'existait pas, les MO inactivés étaient des `ingrédients autres`
            strain=teleIcare_microorganism.ingmorg_souche or "",
            quantity=teleIcare_microorganism.ingmorg_quantite_par_djr,
        )
        return declared_microorganism
    except Microorganism.DoesNotExist as e:
        logger.error(e)
        return


def create_declared_ingredient(declaration, teleIcare_ingredient, active):
    try:
        declared_ingredient = DeclaredIngredient(
            declaration=declaration,
            ingredient=Ingredient.objects.get(siccrf_id=teleIcare_ingredient.inga_ident),
            active=active,
            quantity=None,  # dans TeleIcare, les ingrédients n'avaient pas de quantité associée
        )
        return declared_ingredient
    except Ingredient.DoesNotExist as e:
        logger.error(e)
        return


def create_computed_substance(declaration, teleIcare_substance):
    try:
        computed_substance = ComputedSubstance(
            declaration=declaration,
            substance=Substance.objects.get(siccrf_id=teleIcare_substance.sbsact_ident),
            quantity=teleIcare_substance.sbsactdecl_quantite_par_djr,
            # le champ de TeleIcare 'sbsact_commentaires' n'est pas repris
        )
        return computed_substance
    except Substance.DoesNotExist as e:
        logger.error(e)
        return


@transaction.atomic
def add_product_info_from_teleicare_history(declaration, vrsdecl_ident):
    """
    Cette function importe les champs ManyToMany des déclarations, relatifs à l'onglet "Produit"
    Il est nécessaire que les objets soient enregistrés en base (et aient obtenu un id) grâce à la fonction
    `create_declarations_from_teleicare_history` pour updater leurs champs ManyToMany.
    """
    # aucun des champs `other_` n'est rempli dans Teleicare
    # IcaPopulationCibleDeclaree.vrspcb_popcible_autre n'est pas importé car vide
    # IcaPopulationRisqueDeclaree.vrsprs_poprisque_autre n'est pas importé car vide
    # IcaEffetDeclare.vrs_autre_objectif n'est pas importé car vide
    declaration.effects.set(
        [
            Effect.objects.get(siccrf_id=TIcare_effect.objeff_ident)
            for TIcare_effect in IcaEffetDeclare.objects.filter(vrsdecl_ident=vrsdecl_ident)
        ]
    )
    declaration.conditions_not_recommended.set(
        [
            Condition.objects.get(siccrf_id=TIcare_condition.poprs_ident)
            for TIcare_condition in IcaPopulationRisqueDeclaree.objects.filter(vrsdecl_ident=vrsdecl_ident)
        ]
    )

    teleicare_population_ids = IcaPopulationCibleDeclaree.objects.filter(vrsdecl_ident=vrsdecl_ident).values_list(
        "popcbl_ident", flat=True
    )
    if teleicare_population_ids.exists():
        declaration.populations.set(get_CA_corresponding_population(teleicare_population_ids))


@transaction.atomic
def add_composition_from_teleicare_history(declaration, vrsdecl_ident):
    """
    Cette function importe les champs ManyToMany des déclarations, relatifs à l'onglet "Composition"
    Il est nécessaire que les objets soient enregistrés en base (et aient obtenu un id) grâce à la fonction
    `create_declarations_from_teleicare_history` pour updater leurs champs ManyToMany.
    """
    bulk_ingredients = {DeclaredPlant: [], DeclaredMicroorganism: [], DeclaredIngredient: [], ComputedSubstance: []}
    for ingredient in IcaIngredient.objects.filter(vrsdecl_ident=vrsdecl_ident):
        if ingredient.tying_ident == 1:
            declared_plant = create_declared_plant(
                declaration=declaration,
                teleIcare_plant=IcaPreparation.objects.get(
                    ingr_ident=ingredient.ingr_ident,
                ),
                active=ingredient.fctingr_ident == 1,
            )
            if declared_plant:
                bulk_ingredients[DeclaredPlant].append(declared_plant)
        elif ingredient.tying_ident == 2:
            declared_microorganism = create_declared_microorganism(
                declaration=declaration,
                teleIcare_microorganism=IcaMicroOrganisme.objects.get(
                    ingr_ident=ingredient.ingr_ident,
                ),
                active=ingredient.fctingr_ident == 1,
            )
            if declared_microorganism:
                bulk_ingredients[DeclaredMicroorganism].append(declared_microorganism)
        elif ingredient.tying_ident == 3:
            declared_ingredient = create_declared_ingredient(
                declaration=declaration,
                teleIcare_ingredient=IcaIngredientAutre.objects.get(
                    ingr_ident=ingredient.ingr_ident,
                ),
                active=ingredient.fctingr_ident == 1,
            )
            if declared_ingredient:
                bulk_ingredients[DeclaredIngredient].append(declared_ingredient)
    # dans TeleIcare les `declared_substances` étaient des ingrédients
    # donc on ne rempli pas le champ declaration.declared_substances grâce à l'historique
    for teleIcare_substance in IcaSubstanceDeclaree.objects.filter(vrsdecl_ident=vrsdecl_ident):
        computed_substance = create_computed_substance(
            declaration=declaration, teleIcare_substance=teleIcare_substance
        )
        if computed_substance:
            bulk_ingredients[ComputedSubstance].append(computed_substance)

    for model, bulk_of_objects in bulk_ingredients.items():
        model.objects.bulk_create(bulk_of_objects)


def compute_action(status, nb_version_declaration):
    if status == Declaration.DeclarationStatus.WITHDRAWN:
        return Snapshot.SnapshotActions.WITHDRAW
    elif status == Declaration.DeclarationStatus.REJECTED:
        return Snapshot.SnapshotActions.ACCEPT_VISA  # les rejets arrivent seulement sur visa
    elif status == Declaration.DeclarationStatus.ABANDONED:
        return Snapshot.SnapshotActions.ABANDON
    elif status == Declaration.DeclarationStatus.AUTHORIZED and nb_version_declaration == 1:
        return Snapshot.SnapshotActions.SUBMIT
    else:
        return Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION  # pourrait aussi être une RESPOND_TO_OBJECTION


last_word_to_administration_status = (Declaration.DeclarationStatus.REJECTED, Snapshot.SnapshotActions.ABANDON)


@transaction.atomic
def add_final_state_snapshot(
    declaration,
    latest_ica_version_declaration,
    declaration_acceptation_date,
    nb_version_declaration,
    effective_withdrawal_date=None,
):
    if not declaration.snapshots.exists():
        snapshot = Snapshot(
            creation_date=declaration_acceptation_date,
            modification_date=declaration_acceptation_date,
            declaration=declaration,
            status=declaration.status,
            json_declaration="",
            # le commentaire est soit celui de l'administration `vrsdecl_observations_ac` soit celui du pro `vrsdecl_commentaires`
            comment=latest_ica_version_declaration.vrsdecl_observations_ac
            if declaration.status in last_word_to_administration_status
            else latest_ica_version_declaration.vrsdecl_commentaires or "",
            action=compute_action(declaration.status, nb_version_declaration),
            post_validation_status=Declaration.DeclarationStatus.AUTHORIZED,
        )
        with suppress_autotime(snapshot, ["creation_date", "modification_date"]):
            snapshot.save()


def create_declarations_from_teleicare_history(company_ids=[], rewrite_existing=False):
    """
    Dans Teleicare une entreprise peut-être relié à une déclaration par 3 relations différentes :
    * responsable de l'étiquetage (équivalent Declaration.mandated_company)
    * gestionnaire de la déclaration (équivalent Declaration.company)
    * télédéclarante de la déclaration (cette relation n'est pour le moment pas conservée, car le BEPIAS ne sait pas ce qu'elle signifie)
    """
    nb_created_declarations = 0

    etab_ids = (
        EtablissementToCompanyRelation.objects.exclude(siccrf_id=None)
        if not company_ids
        else EtablissementToCompanyRelation.objects.filter(company_id__in=company_ids)
    ).values_list("siccrf_id", flat=True)
    # Parcourir tous les compléments alimentaires dont l'entreprise déclarante a été matchée
    for ica_complement_alimentaire in IcaComplementAlimentaire.objects.filter(etab_id__in=etab_ids):
        all_ica_declarations = IcaDeclaration.objects.filter(
            cplalim_id=ica_complement_alimentaire.cplalim_ident
        ).exclude(icaversiondeclaration__isnull=True)  # la déclaration doit être liée à une version de déclaration

        if all_ica_declarations.exists():
            # retrouve la déclaration la plus à jour correspondant à ce complément alimentaire
            oldest_ica_declaration, latest_ica_declaration = get_oldest_and_latest(all_ica_declarations)

            # retrouve la version de déclaration la plus à jour correspondant à cette déclaration
            declaration_versions = IcaVersionDeclaration.objects.filter(
                dcl_id=latest_ica_declaration.dcl_ident,
                stattdcl_ident__in=[
                    2,
                    5,
                    6,
                    8,
                ],  # status 'autorisé', 'refusé', 'arrêt commercialisation', 'abandonné'
                stadcl_ident=8,  # état 'clos'
            )
            nb_version_declaration = declaration_versions.count()
            latest_ica_version_declaration = declaration_versions.order_by("vrsdecl_numero").last()
            # la déclaration a une version finalisée
            if latest_ica_version_declaration:
                try:  # pas possible d'utiliser update_or_create
                    declaration = Declaration.objects.get(
                        siccrf_id=ica_complement_alimentaire.cplalim_ident,
                        # resp mise sur le marché (entreprise qui déclare ou pour laquelle une entreprise mandataire déclare)
                    )
                    if not rewrite_existing:
                        continue
                except Declaration.DoesNotExist:
                    declaration = Declaration(
                        siccrf_id=ica_complement_alimentaire.cplalim_ident,
                        # resp mise sur le marché (entreprise qui déclare ou pour laquelle une entreprise mandataire déclare)
                        company=EtablissementToCompanyRelation.objects.get(
                            siccrf_id=ica_complement_alimentaire.etab_id
                        ).company,
                    )
                declaration_attrs = compute_declaration_attributes(
                    ica_complement_alimentaire, latest_ica_declaration, latest_ica_version_declaration
                )
                for key, value in declaration_attrs.items():
                    declaration.__setattr__(key, value)

                declaration.creation_date = (
                    convert_str_date(oldest_ica_declaration.dcl_date, aware=True)
                    if oldest_ica_declaration.dcl_date
                    else ""
                )
                declaration_acceptation_date = (
                    convert_str_date(latest_ica_declaration.dcl_date, aware=True)
                    if latest_ica_declaration.dcl_date
                    else ""
                )
                effective_withdrawal_date = (
                    convert_str_date(latest_ica_declaration.dcl_date_fin_commercialisation, aware=True)
                    if latest_ica_declaration.dcl_date_fin_commercialisation
                    else None
                )
                # la date de modification est la date de fin de commercialisation si elle existe ou la date d'acceptation
                declaration.modification_date = (
                    effective_withdrawal_date if effective_withdrawal_date else declaration_acceptation_date
                )

                with suppress_autotime(declaration, ["creation_date", "modification_date"]):
                    declaration.save()

                    add_product_info_from_teleicare_history(declaration, latest_ica_version_declaration.vrsdecl_ident)
                    add_composition_from_teleicare_history(declaration, latest_ica_version_declaration.vrsdecl_ident)
                    add_final_state_snapshot(
                        declaration,
                        latest_ica_version_declaration,
                        declaration_acceptation_date,
                        nb_version_declaration,
                        effective_withdrawal_date=effective_withdrawal_date,
                    )
                    nb_created_declarations += 1

    logger.info(f"Sur {len(IcaComplementAlimentaire.objects.all())} : {nb_created_declarations} déclarations créées.")
