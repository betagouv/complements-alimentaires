def all_true_or_all_false(*values):
    """Return True if given values are either all truthy, or all falsy."""

    values = [bool(value) for value in values]
    return len(set(values)) == 1
