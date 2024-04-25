from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password

from rest_framework import serializers

from data.models.roles import CompanySupervisor, Declarant
from data.utils.dict_utils import invert_dict

from .company import SimpleCompanySerializer
from .roles import CompanySupervisorSerializer, DeclarantSerializer

User = get_user_model()


class BlogPostAuthor(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


role_serializer_mapping = {CompanySupervisor: CompanySupervisorSerializer, Declarant: DeclarantSerializer}


class StaffUserSerializer(serializers.ModelSerializer):
    """Retourne un utilisateur d'une entreprise donnée.
    Utilisé actuellement pour afficher la liste des collaborateurs d'une entreprise spécifique"""

    class Meta:
        model = User
        fields = ("id", "username", "email", "last_name", "first_name", "roles")

    id = serializers.IntegerField(read_only=True)
    roles = serializers.SerializerMethodField(read_only=True)  # Roles d'une entreprise donnée

    def get_roles(self, obj):
        company_id = self.context["company_id"]
        role_classes = [Declarant, CompanySupervisor]

        roles = []
        for role_class in role_classes:
            queryset = role_class.objects.filter(user=obj, companies=company_id)
            if queryset.exists():
                roles.append(role_serializer_mapping[role_class](queryset.get()).data)

        return roles


class UserSerializer(serializers.ModelSerializer):
    """Retourne un utilisateur avec toutes les entreprises dans lesquelles il a un rôle.
    Utilisé actuellement pour l'utilisateur connecté (loggedUser)
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "last_name", "first_name", "companies")

    id = serializers.IntegerField(read_only=True)
    companies = serializers.SerializerMethodField(read_only=True)  # entreprises + roles par entreprise

    def get_companies(self, obj):
        """
        Organise les données des rôles par entreprise - ce qui n'est pas l'organisation naturelle de la modélisation.
        TODO: code pas du tout optimisé, et trop complexe -> essayer de faire même logique que get_roles()
        NOTE: il manquera les potentiels futurs autres rôles qui ne seront pas liés à des companies.
        """

        data = {(role.id, role._meta.model): role.companies.values_list("id", flat=True) for role in obj.roles()}
        # ex : {(2, data.models.roles.CompanySupervisor): <CompanyQuerySet [2]>,
        #       (3, data.models.roles.Declarant): <CompanyQuerySet [1, 2, 3]>}

        data = invert_dict(data)
        # ex: {2: [(2, data.models.roles.CompanySupervisor), (3, data.models.roles.Declarant)],
        #      1: [(3, data.models.roles.Declarant)],
        #      3: [(3, data.models.roles.Declarant)]}

        from data.models import Company  # évite un import circulaire

        result = []
        for company_id, role_tuples in data.items():
            # Récupère les données sérializées de la company
            company_data_dict = SimpleCompanySerializer(Company.objects.get(id=company_id)).data

            # Récupère les données sérializées des roles
            role_data = [
                role_serializer_mapping[role_class](role_class.objects.get(id=role_id)).data
                for role_id, role_class in role_tuples
            ]

            # Merge les deux types de données
            result.append(company_data_dict | {"roles": role_data})

        return result


class CreateUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ("password",)

    password = serializers.CharField(
        write_only=True, required=True
    )  # empêche le retour du hash du mdp dans la réponse

    def validate_password(self, value):
        """Validate the password against settings-defined rules"""
        django_validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"confirm_new_password": "La confirmation ne correspond pas au mot de passe entré"}
            )
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "Le nouveau mot de passe est identique à l'actuel"})
        django_validate_password(data["new_password"])
        return data
