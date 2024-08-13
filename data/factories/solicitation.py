import random

import factory

from data.models import CollaborationInvitation, CompanyAccessClaim, SupervisionClaim
from data.models.company import CompanyRoleClassChoices

from .company import CompanyFactory, SupervisorRoleFactory
from .user import UserFactory


class BaseSolicitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    sender = factory.SubFactory(UserFactory)


class SupervisionClaimFactory(BaseSolicitationFactory):
    class Meta:
        model = SupervisionClaim

    personal_msg = "Je suis créateur de cette entreprise."
    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def recipients(self, create, extracted, **kwargs):
        """Surchargé pour que les destinataires ajoutés soient bien du staff"""
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for recipient in extracted:
                self.recipients.add(recipient)
        else:
            for _ in range(3):
                self.recipients.add(UserFactory(is_staff=True))


class CompanyAccessClaimFactory(BaseSolicitationFactory):
    class Meta:
        model = CompanyAccessClaim

    personal_msg = "Merci d'accepter ma demande pour gérer à vos côtés."
    declarant_role = True
    supervisor_role = True

    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def recipients(self, create, extracted, **kwargs):
        """Surchargé pour que les destinataires ajoutés soient bien gestionnaires"""
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for recipient in extracted:
                self.recipients.add(recipient)
        else:
            for _ in range(3):
                supervisor_role = SupervisorRoleFactory(company=self.company)
                self.recipients.add(supervisor_role.user)


class CollaborationInvitationFactory(BaseSolicitationFactory):
    class Meta:
        model = CollaborationInvitation

    def _make_roles() -> list[str]:
        nb_roles = random.randint(1, len(list(CompanyRoleClassChoices)))
        return random.sample(list(CompanyRoleClassChoices), nb_roles)

    personal_msg = ""
    recipient_email = factory.Faker("email")
    company = factory.SubFactory(CompanyFactory)
    roles = factory.LazyFunction(_make_roles)
