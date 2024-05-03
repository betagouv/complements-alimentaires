import factory

from data.models.solicitation import Solicitation, SolicitationKindChoices

from .company import CompanyFactory
from .user import UserFactory


class SolicitationFactory(factory.django.DjangoModelFactory):
    """
    Chaque solicitation étant trop différente l'une de l'autre (différents arguments pour leur création),
    cette classe reste abstraite, et on devra définir quelle solicitation (concrète) créer.
    """

    class Meta:
        model = Solicitation
        abstract = True

    sender = factory.SubFactory(UserFactory)

    @factory.post_generation
    def recipients(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for recipient in extracted:
                self.recipients.add(recipient)
        else:
            for _ in range(3):
                self.recipients.add(UserFactory())


class BaseCompanyWithSupervisionFactory(SolicitationFactory):
    company = factory.SubFactory(CompanyFactory)

    # TODO: fix cette erreur - on veut que les users aient les droits de Supervisor
    # de la company utilisée - sauf que l'attribut n'existe pas sur l'objet créé

    # @factory.post_generation
    # def recipients(self, create, extracted, **kwargs):
    #     """Surchargé pour gérer le fait que les destinataires ajoutés soient bien gestionnaires"""
    #     if not create:
    #         return
    #     if extracted or isinstance(extracted, list):
    #         for recipient in extracted:
    #             self.recipients.add(recipient)
    #     else:
    #         for _ in range(3):
    #             supervisor_role = SupervisorRoleFactory(company=self.company)
    #             self.recipients.add(supervisor_role.user)


class RequestSupervisionFactory(BaseCompanyWithSupervisionFactory):
    kind = SolicitationKindChoices.RequestSupervision


class RequestCoSupervisionFactory(BaseCompanyWithSupervisionFactory):
    kind = SolicitationKindChoices.RequestCoSupervision


class InviteCoSupervision(BaseCompanyWithSupervisionFactory):
    kind = SolicitationKindChoices.InviteCoSupervision
