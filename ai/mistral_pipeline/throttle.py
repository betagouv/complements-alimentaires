# Mistral enforces a requests per second limit and a tokens per minute limit,
# both per organisation and per model, and their values are only readable from
# the admin panel. Rather than encoding limits we cannot know here, calls are
# simply spaced out and a 429 is waited out: the token window slides over a
# minute, so a pause of that order is enough to get through.
import re
import time
from functools import wraps

DEFAULT_THROTTLE = {
    # seconds to leave between the end of a call and the start of the next one
    "min_interval": 2.0,
    "max_retries": 4,
    # seconds waited after a first 429, doubled at every further one
    "first_backoff": 30.0,
    "backoff_factor": 2.0,
    "max_backoff": 120.0,
}

THROTTLE = dict(DEFAULT_THROTTLE)

RATE_LIMIT_STATUS = 429
# the SDK wraps the response in an exception whose string starts with
# "API error occurred: Status 429."
STATUS_IN_MESSAGE_REGEX = re.compile(r"\b429\b")

_last_call_ended_at = None


def configure(**overrides):
    unknown = sorted(set(overrides) - set(DEFAULT_THROTTLE))
    if unknown:
        raise ValueError(f"Unknown throttle settings: {', '.join(unknown)}")
    THROTTLE.update(overrides)


def reset():
    global _last_call_ended_at
    _last_call_ended_at = None
    THROTTLE.clear()
    THROTTLE.update(DEFAULT_THROTTLE)


def _wait_for_slot():
    if _last_call_ended_at is None:
        return
    remaining = THROTTLE["min_interval"] - (time.monotonic() - _last_call_ended_at)
    if remaining > 0:
        time.sleep(remaining)


def is_rate_limited(error):
    if getattr(error, "status_code", None) == RATE_LIMIT_STATUS:
        return True
    return bool(STATUS_IN_MESSAGE_REGEX.search(str(error)))


# the API may tell us how long to wait, in which case we trust it over our own
# backoff
def retry_after(error):
    response = getattr(error, "raw_response", None)
    headers = getattr(response, "headers", None) or getattr(error, "headers", None)
    if not headers:
        return None
    try:
        value = headers.get("retry-after")
    except AttributeError:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# every function calling the Mistral API goes through here, so that the pauses
# are counted across the whole pipeline rather than per call site
def throttled(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        global _last_call_ended_at
        retries = 0
        backoff = THROTTLE["first_backoff"]
        while True:
            _wait_for_slot()
            try:
                return function(*args, **kwargs)
            except Exception as error:
                if retries >= THROTTLE["max_retries"] or not is_rate_limited(error):
                    raise
                retries += 1
                pause = retry_after(error) or backoff
                print(f"Rate limited by Mistral, waiting {pause:.0f}s before retry {retries}/{THROTTLE['max_retries']}")
                time.sleep(pause)
                backoff = min(backoff * THROTTLE["backoff_factor"], THROTTLE["max_backoff"])
            finally:
                _last_call_ended_at = time.monotonic()

    return wrapper
