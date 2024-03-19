import random
import string


def make_random_str(size: int, chars: str = string.printable) -> str:
    """Build a random string of `size`, using `chars`."""
    return "".join(random.choice(chars) for _ in range(size))
