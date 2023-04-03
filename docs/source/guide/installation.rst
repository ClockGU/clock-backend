.. _installation:

Installation
================


.. _local-installation:

Local Installation
------------------

The CLOCK-Backend is running in docker containers. To run it locally follow these steps:

.. code-block:: bash

    # Starting the containers
    $ docker-compose up

    # Migrate settings made by django.
    $ docker-compose run --rm web python manage.py migrate

    # Create a superuse for the amdin
    $ docker-compose run --rm web python manage.py createsuperuser


Then open `<http://localhost:8000/admin>`_:

#. Create an entry in 'SITES/Sites' with the Domain you want to use with ID 1.

#. Create an entry in 'SOCIAL ACCOUNTS/Social applications' if you want to use external authentication lice CAS for the Goethe University Frankfurt.