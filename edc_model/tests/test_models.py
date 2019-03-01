from copy import copy
from django.apps import apps as django_apps
from django.test import TestCase, tag  # noqa
from django.test.utils import override_settings
from django.core.exceptions import ImproperlyConfigured

from ..models import UrlModelMixinNoReverseMatch
from .models import TestBaseModel, TestSimpleModel


class TestModels(TestCase):
    @override_settings(USE_TZ=False)
    def test_tz(self):
        app_config = django_apps.get_app_config("edc_model")
        self.assertRaises(ImproperlyConfigured, app_config.ready)

    def test_base_update_fields(self):
        """Assert update fields cannot bypass modified fields.
        """
        obj = TestBaseModel.objects.create()
        modified = copy(obj.modified)

        obj.save(update_fields=["f1"])
        obj.refresh_from_db()

        self.assertNotEqual(modified, obj.modified)

    def test_base_verbose_name(self):
        obj = TestBaseModel.objects.create()
        self.assertEqual(obj.verbose_name, obj._meta.verbose_name)

    def test_get_absolute_url_change(self):
        obj = TestBaseModel.objects.create()
        self.assertEqual(
            obj.get_absolute_url(), "/admin/edc_model/testbasemodel/1/change/"
        )

    def test_get_absolute_url_add(self):
        obj = TestBaseModel()
        self.assertEqual(obj.get_absolute_url(), "/admin/edc_model/testbasemodel/add/")

    def test_get_absolute_url_not_registered(self):
        obj = TestSimpleModel()
        self.assertRaises(UrlModelMixinNoReverseMatch, obj.get_absolute_url)
