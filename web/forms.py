from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "Agnès", "autocomplete": "given-name"}, autoFocus=True
        )
        self.fields["last_name"].widget.attrs.update({"placeholder": "Dufresne", "autocomplete": "family-name"})
        self.fields["username"].widget.attrs.update({"placeholder": "agnes.dufresne"})
        self.fields["email"].widget.attrs.update({"placeholder": "agnes.d@example.com", "autocomplete": "email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Entrez votre mot de passe"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirmez votre mot de passe"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = get_user_model().objects.normalize_email(self.cleaned_data.get("email"))

        if commit:
            user.save()

        return user
