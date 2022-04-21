.. _installation:

Installation
================


.. _local-installation:

Local Installation
------------------

The CLOCK-Backend is running in docker containers. To run it localy you have to follow these steps:

.. code-block:: bash

    $ docker-compose up

    $ docker-compose run --rm web python manage.py migrate

    $ docker-compose run --rm web python manage.py createsuperuser


