import random
import string

import factory
import faker
from phonenumber_field.phonenumber import PhoneNumber

from data.choices import CountryChoices
from data.models.teleicare_history.ica_etablissement import IcaEtablissement
from data.utils.string_utils import make_random_str
from data.factories.company import _make_siret, _make_vat, _make_phone_number


class EtablissementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IcaEtablissement

    etab_ident = factory.Sequence(lambda n: n + 1)
    etab_raison_sociale = factory.Faker("company", locale="FR")
    etab_enseigne = factory.Faker("company", locale="FR")
    etab_siret = factory.LazyFunction(_make_siret)
    etab_numero_tva_intra = factory.LazyFunction(_make_siret)
    pays_ident = factory.Faker("pyint", min_value=0, max_value=200)
    etab_nb_compte_autorise = factory.Faker("pyint", min_value=0, max_value=5)
    # contact
    etab_telephone = factory.LazyFunction(_make_phone_number)
    etab_courriel = factory.Faker("email", locale="FR")
