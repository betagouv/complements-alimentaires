import factory
import string
from django.contrib.auth import get_user_model
from data.utils.string_utils import make_random_str


def _make_username() -> str:
    return "user_" + make_random_str(size=10, chars=string.ascii_letters)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    username = factory.LazyFunction(_make_username)
    password = "abcdefg123$"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default way to create user objects."""
        manager = cls._get_manager(model_class)
        # The default would use `manager.create(*args, **kwargs)`
        return manager.create_user(*args, **kwargs)
