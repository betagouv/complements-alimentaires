from api.exception_handling import ProjectAPIException


class CSVFileError(Exception):
    """Raised when the input CSV is not valid"""

    def __init__(self, message, traceback=None):
        self.message = message
        self.traceback = traceback


class InvalidEmail(ProjectAPIException):
    field_errors = {"email": "L'email fourni est invalide."}


class EmailAlreadyExists(ProjectAPIException):
    field_errors = {"email": "L'adresse e-mail renseignée existe déjà."}
