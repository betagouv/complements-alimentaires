from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password

from rest_framework import serializers

from data.models.company import DeclarantRole, SupervisorRole

from .company import DeclarantRoleSerializer, SimpleCompanySerializer, SupervisorRoleSerializer

User = get_user_model()


class BlogPostAuthor(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


role_serializer_mapping = {SupervisorRole: SupervisorRoleSerializer, DeclarantRole: DeclarantRoleSerializer}


class CollaboratorSerializer(serializers.ModelSerializer):
    """Retourne un utilisateur d'une entreprise donnée.
    Utilisé actuellement pour afficher la liste des collaborateurs d'une entreprise spécifique"""

    class Meta:
        model = User
        fields = ("id", "username", "email", "last_name", "first_name", "roles")

    id = serializers.IntegerField(read_only=True)
    roles = serializers.SerializerMethodField(read_only=True)  # Roles d'une entreprise donnée

    def get_roles(self, obj):
        return [
            role_serializer_mapping[type(role)](role).data for role in obj.company_roles(self.context["company_id"])
        ]


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
        from data.models import Company  # évite un import circulaire

        result = []
        for company_id, roles in obj.all_company_roles().items():
            company_data_dict = SimpleCompanySerializer(Company.objects.get(id=company_id)).data
            role_data = [role_serializer_mapping[type(role)](role).data for role in roles]
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
