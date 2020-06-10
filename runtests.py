#!/usr/bin/env python
import django
import logging
import os
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from os.path import abspath, dirname, join

from edc_test_utils import DefaultTestSettings
from multisite import SiteID


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


base_dir = dirname(abspath(__file__))
app_name = "edc_model"

DEFAULT_SETTINGS = DefaultTestSettings(
    APP_NAME="edc_model",
    BASE_DIR=base_dir,
    SITE_ID=SiteID(default=1),
    ALLOWED_HOSTS=["localhost"],
    ROOT_URLCONF=f"{app_name}.tests.urls",
    STATIC_URL="/static/",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "multisite",
        "edc_device.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_model.apps.AppConfig",
    ],
).settings

if os.environ.get("TRAVIS"):
    DEFAULT_SETTINGS.update(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "edc",
                "USER": "travis",
                "PASSWORD": "",
                "HOST": "localhost",
                "PORT": "",
            },
            "client": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "edc_client",
                "USER": "travis",
                "PASSWORD": "",
                "HOST": "localhost",
                "PORT": "",
            },
        }
    )


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests(
        [f"{app_name}.tests"]
    )
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
