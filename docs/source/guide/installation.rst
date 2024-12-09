.. _installation:

Installation
================


.. _local-installation:

Local Installation
------------------

The CLOCK-Backend is running in docker containers. To run it locally follow these steps:

.. code-block:: bash

    # Starting the containers
    $ docker compose up

    # Migrate settings made by django.
    $ docker compose run --rm web python manage.py migrate

    # Create a superuser for the admin
    $ docker compose run --rm web python manage.py createsuperuser


Then open `<http://localhost:8000/admin>`_:

#. Modify the existing entry `"example.com"` in 'SITES/Sites' with the Domain `"preview.clock.uni-frankfurt.de"` or a different one you want to use with ID 1.

#. Create an entry in 'SOCIAL ACCOUNTS/Social applications' if you want to use external authentication lice CAS for the Goethe University Frankfurt (Credentials available on Hessenbox for HR-PS employees).
Other authentications services are possible, see `django-allauth <https://docs.allauth.org/en/latest/>`_.