def yes_or_no(question) -> bool:
    """
    Input the given yes/no question to a user, and returns the result as boolean.
    """
    reply = str(input(question + " Continue? (y/n): ")).lower().strip()
    return bool(reply == "y")
