from api.exception_handling import ProjectAPIException


class CSVFileError(Exception):
    """Raised when the input CSV is not valid"""

    def __init__(self, message, traceback=None):
        self.message = message
        self.traceback = traceback


class EmailAlreadyExists(ProjectAPIException):
    default_detail = "L'adresse e-mail renseignée existe déjà."
    display = "field"
    field_name = "email"


class UnknownSIBError(ProjectAPIException):
    default_detail = "Une erreur inconnue avec l'API SendInBlue a eu lieu."
    display = "global"
