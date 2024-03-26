from .exception_handling import ProjectAPIException


class InvalidEmail(ProjectAPIException):
    field_errors = {"email": "L'email fourni est invalide."}


class EmailAlreadyExists(ProjectAPIException):
    field_errors = {"email": "L'adresse e-mail renseignée existe déjà."}
