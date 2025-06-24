import random
import string

import factory
import faker

from phonenumber_field.phonenumber import PhoneNumber
from datetime import datetime, timedelta
from random import randrange

from data.choices import CountryChoices
from data.models.teleicare_history.ica_etablissement import IcaEtablissement
from data.models.teleicare_history.ica_declaration import (
    IcaComplementAlimentaire,
    IcaDeclaration,
    IcaVersionDeclaration,
    IcaPopulationCibleDeclaree,
)
from data.models.teleicare_history.ica_declaration_composition import (
    IcaIngredient,
    IcaIngredientAutre,
    IcaMicroOrganisme,
    IcaPreparation,
    IcaSubstanceDeclaree,
)
from data.utils.string_utils import make_random_str
from data.factories.company import _make_siret, _make_vat, _make_phone_number


def random_date(start, end=datetime.now()):
    """
    Retourne une date random entre une date de début et une date de fin
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


class EtablissementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaEtablissement

    etab_ident = factory.Sequence(lambda n: n + 1)
    etab_raison_sociale = factory.Faker("company", locale="FR")
    etab_enseigne = factory.Faker("company", locale="FR")
    etab_siret = factory.LazyFunction(_make_siret)
    etab_numero_tva_intra = factory.LazyFunction(_make_vat)
    pays_ident = factory.Faker("pyint", min_value=0, max_value=200)
    etab_nb_compte_autorise = factory.Faker("pyint", min_value=0, max_value=5)
    # contact
    etab_telephone = factory.LazyFunction(_make_phone_number)
    etab_courriel = factory.Faker("email", locale="FR")
    etab_adre_ville = factory.Faker("city", locale="FR")
    etab_adre_cp = factory.Faker("postcode", locale="FR")
    etab_adre_voie = factory.Faker("street_address", locale="FR")
    etab_date_adhesion = datetime.strftime(random_date(start=datetime(2016, 1, 1)), "%m/%d/%Y %H:%M:%S %p")


class ComplementAlimentaireFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaComplementAlimentaire

    cplalim_ident = factory.Sequence(lambda n: n + 1)
    frmgal_ident = factory.Faker("pyint", min_value=0, max_value=20)
    etab = factory.SubFactory(EtablissementFactory)
    cplalim_marque = factory.Faker("text", max_nb_chars=20)
    cplalim_gamme = factory.Faker("text", max_nb_chars=20)
    cplalim_nom = factory.Faker("text", max_nb_chars=20)
    dclencours_gout_arome_parfum = factory.Faker("text", max_nb_chars=20)
    cplalim_forme_galenique_autre = factory.Faker("text", max_nb_chars=20)


class DeclarationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaDeclaration

    dcl_ident = factory.Sequence(lambda n: n + 1)
    cplalim = factory.SubFactory(ComplementAlimentaireFactory)
    # 3 valeurs possibles dans TeleIcare {1: "Article 15", 2: "Article 16", 3: "Simplifiée"}
    tydcl_ident = factory.Faker("pyint", min_value=1, max_value=3)
    etab = factory.SubFactory(EtablissementFactory)
    etab_ident_rmm_declarant = factory.Faker("pyint", min_value=0, max_value=20)
    dcl_date = datetime.strftime(random_date(start=datetime(2016, 1, 1)), "%m/%d/%Y %H:%M:%S %p")
    dcl_date_fin_commercialisation = factory.LazyFunction(
        lambda: datetime.strftime(random_date(start=datetime(2016, 1, 1)), "%m/%d/%Y %H:%M:%S %p")
        if random.random() > 0.3
        else None
    )


class VersionDeclarationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaVersionDeclaration

    vrsdecl_ident = factory.Sequence(lambda n: n + 1)
    ag_ident = factory.Faker("pyint", min_value=0, max_value=20)
    typvrs_ident = factory.Faker("pyint", min_value=0, max_value=20)
    unt_ident = factory.Faker("pyint", min_value=0, max_value=20)
    pays_ident_adre = factory.Faker("pyint", min_value=0, max_value=8)
    etab = factory.SubFactory(EtablissementFactory)
    pays_ident_pays_de_reference = factory.Faker("pyint", min_value=0, max_value=8)
    dcl = factory.SubFactory(DeclarationFactory)
    stattdcl_ident = factory.Faker("pyint", min_value=0, max_value=8)
    stadcl_ident = factory.Faker("pyint", min_value=0, max_value=8)
    vrsdecl_numero = factory.Faker("pyint", min_value=0, max_value=20)
    vrsdecl_commentaires = factory.Faker("text", max_nb_chars=20)
    vrsdecl_mise_en_garde = factory.Faker("text", max_nb_chars=20)
    vrsdecl_durabilite = factory.Faker("pyint", min_value=0, max_value=8)
    vrsdecl_mode_emploi = factory.Faker("text", max_nb_chars=20)
    vrsdecl_djr = factory.fuzzy.FuzzyText(length=4, chars=string.ascii_uppercase + string.digits)
    vrsdecl_conditionnement = factory.Faker("text", max_nb_chars=20)
    vrsdecl_poids_uc = factory.Faker("pyfloat")
    vrsdecl_forme_galenique_autre = factory.Faker("text", max_nb_chars=20)
    vrsdecl_date_limite_reponse_pro = factory.Faker("text", max_nb_chars=20)
    vrsdecl_observations_ac = factory.Faker("text", max_nb_chars=20)
    vrsdecl_observations_pro = factory.Faker("text", max_nb_chars=20)
    vrsdecl_numero_dossiel = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_ville = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_cp = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_voie = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_comp = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_comp2 = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_dist = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_region = factory.Faker("text", max_nb_chars=20)
    vrsdecl_adre_raison_sociale = factory.Faker("text", max_nb_chars=20)


class IcaPopulationCibleDeclareeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaPopulationCibleDeclaree

    vrsdecl_ident = factory.Sequence(lambda n: n + 1)
    popcbl_ident = factory.Sequence(lambda n: n + 1)
    vrspcb_popcible_autre = factory.Faker("text", max_nb_chars=20)


class IcaIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaIngredient

    ingr_ident = factory.Sequence(lambda n: n + 1)
    vrsdecl_ident = factory.Sequence(lambda n: n + 1)
    fctingr_ident = factory.Faker("pyint", min_value=1, max_value=3)
    tying_ident = factory.Faker("pyint", min_value=1, max_value=3)  # 1 = Ingredient, 2 = Microorganism, 3 = Plant
    ingr_commentaires = factory.Faker("text", max_nb_chars=20)


class IcaIngredientAutreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaIngredientAutre

    ingr_ident = factory.SubFactory(IcaIngredient)
    inga_ident = factory.Faker("pyint", min_value=1, max_value=20)


class IcaMicroOrganismeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaMicroOrganisme

    ingr_ident = factory.SubFactory(IcaIngredient)
    morg_ident = factory.Faker("pyint", min_value=1, max_value=20)
    ingmorg_souche = factory.Faker("text", max_nb_chars=10)
    ingmorg_quantite_par_djr = factory.Faker("pyfloat")


class IcaPreparationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaPreparation

    ingr_ident = factory.SubFactory(IcaIngredient)
    plte_ident = factory.Faker("pyint", min_value=1, max_value=20)
    pplan_ident = factory.Faker("pyint", min_value=1, max_value=20)
    unt_ident = factory.Faker("pyint", min_value=1, max_value=5)
    typprep_ident = factory.Faker("pyint", min_value=1, max_value=20)
    prepa_qte = factory.Faker("pyfloat")


class IcaSubstanceDeclareeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaSubstanceDeclaree

    vrsdecl_ident = factory.Sequence(lambda n: n + 1)
    sbsact_ident = factory.Faker("pyint", min_value=1, max_value=20)
    sbsact_commentaires = factory.Faker("text", max_nb_chars=20)
    sbsactdecl_quantite_par_djr = factory.Faker("pyfloat")
