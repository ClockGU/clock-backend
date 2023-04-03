.. _api-package:

api package
===========


.. _api-admin:

admin
----------------

Setting up the default Django admin page.

.. automodule:: api.admin
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-apps:

apps
---------------

Django default to define the app name.

.. automodule:: api.apps
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-filters:

filters
------------------

Option to add more filters to the Django filters.

.. automodule:: api.filters
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-models:

models
-----------------

Django default to define the main modules for the app.


.. note::

    The user modell of Djangos is using as primary key for default the username, but we want to use the mail address.
    Therefor you can find in models.py an override for the classes `BaseUserManager` and `AbstractUser`.

.. automodule:: api.models
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-permissions:

permissions
----------------------

Additional permission class to manage that only privilege user are able to access there data.

.. automodule:: api.permissions
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-serializers:

serializers
----------------------

Django default formatter to bring Python objects into JSON-Structure and back, including validation.

.. automodule:: api.serializers
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-urls:

urls
---------------

Django default to define the urls of the app.

.. automodule:: api.urls
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-utilities:

utilities
--------------------

Just a bunch of useful functions, including the action_performed receiver functions.

.. automodule:: api.utilities
   :members:
   :undoc-members:
   :show-inheritance:


.. _api-views:

views
----------------

Django default to define the CRUD-interaction functions.

.. note::

    The viewsets of Djangos rest framework are bringing in most of the CRUD functions by default.
    For further information checkout the Documentation of the
    `viewsets <https://www.django-rest-framework.org/api-guide/viewsets/>`_.

.. automodule:: api.views
   :members:
   :undoc-members:
   :show-inheritance:

