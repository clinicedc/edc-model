|pypi| |actions| |codecov| |downloads| |pyup|

edc-model
---------

Base model, manager, field, form and admin classes for Edc.



All models in the Edc use ``BaseUuidModel``

.. code-block:: python

    from edc_model.model_mixins import BaseUuidModel

    class MyModel(BaseUuidModel):

        ....

The mixin:

* sets the id fields to a ``UUIDField`` instead of an integer;
* adds audit fields through ``BaseModel`` (user_created, user_modified, date_created, etc);
* adds ``UrlModelMixin``, ``DeviceModelMixin``

Most models require an audit trail. If so, add the ``HistoricalRecord`` model manager.

.. code-block:: python

    from edc_model.model.models import HistoricalRecord

    class MyModel(BaseUuidModel):

        ...
        history = HistoricalRecord()


``HistoricalRecord`` is an almost identical version of ``simple_history.models.HistoricalRecord``
with the exception of two methods:  ``get_extra_fields()`` and ``add_extra_methods()``. Method
``get_extra_fields()`` is overridden to change the ``history_id`` primary key from an
``IntegerField`` to a ``UUIDField`` so that it can work with module ``django_collect_offline``.


The audit trail models created by ``HistoricalRecord`` have a foreign key to ``auth.User``. In order for the models to work with `django_collect_offline` specify the django_collect_offline User model in settings:

.. code-block:: python

    AUTH_USER_MODEL = 'django_collect_offline.User'


Notes
-----

User created and modified fields behave as follows:

* created is only set on pre-save add
* modified is always updated


.. |pypi| image:: https://img.shields.io/pypi/v/edc-model.svg
    :target: https://pypi.python.org/pypi/edc-model

.. |actions| image:: https://github.com/clinicedc/edc-model/actions/workflows/build.yml/badge.svg
  :target: https://github.com/clinicedc/edc-model/actions/workflows/build.yml

.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-model/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/clinicedc/edc-model

.. |downloads| image:: https://pepy.tech/badge/edc-model
    :target: https://pepy.tech/project/edc-model

.. |pyup| image:: https://pyup.io/repos/github/clinicedc/edc-model/shield.svg
    :target: https://pyup.io/repos/github/clinicedc/edc-model/
    :alt: Updates
