import os
from pathlib import Path

import environ
from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging


@setup_logging.connect
def void(*args, **kwargs):
    """Surcharge le logging de Celery pour l'empêcher de toucher à notre config
    github.com/celery/celery/issues/1867
    """
    pass


# Environment
CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=True)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker=env("REDIS_URL"), backend=env("REDIS_URL"), include=["config.tasks"])
app.worker_hijack_root_logger = False

mornings = crontab(hour=10, minute=0, day_of_week="*")
midnights = crontab(hour=0, minute=0, day_of_week="*")
nightly = crontab(hour=2, minute=0, day_of_week="*")
daily_workweek = crontab(hour=7, minute=0, day_of_week="1-5")

every_minute = crontab(minute="*/1")  # Pour tester en local

app.conf.beat_schedule = {
    "send_expiration_reminder": {
        "task": "config.tasks.send_expiration_reminder",
        "schedule": mornings,
    },
    "expire_declarations": {
        "task": "config.tasks.expire_declarations",
        "schedule": midnights,
    },
    "approve_declarations": {
        "task": "config.tasks.approve_declarations",
        "schedule": daily_workweek,
    },
    "update_market_ready_counts": {
        "task": "config.tasks.update_market_ready_counts",
        "schedule": nightly,
    },
    "export_datasets_to_data_gouv": {
        "task": "config.tasks.export_datasets_to_data_gouv",
        "schedule": midnights,
    },
}

app.conf.timezone = "Europe/Paris"

if __name__ == "__main__":
    app.start()
