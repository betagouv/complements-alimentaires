class CSVFileError(Exception):
    """Raised when the input CSV is not valid"""

    def __init__(self, message, traceback=None):
        self.message = message
        self.traceback = traceback
