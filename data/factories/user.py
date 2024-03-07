import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.Faker("email")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default way to create user objects."""
        manager = cls._get_manager(model_class)
        # The default would use `manager.create(*args, **kwargs)`
        return manager.create_user(*args, **kwargs)
