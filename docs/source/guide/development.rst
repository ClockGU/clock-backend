.. _development:

Development
========================


.. _project_structre:

Project Structure
-------------------------

The CLOCK-Backend is fully designed with Django REST-Framework running in Docker-Containers. You need to install the
Clock-Frontend for interacting with the final Website.


.. _docker-container:

Docker Container
^^^^^^^^^^^^^^^

- DB
    Runs a Postgres-DB.

- Web
    Runs the REST-API.

- Rabbit-Broker
    Queues the async task from the Web-Container and brokers the tasks on the Calery-Worker if threads are available.

- Calery-Worker
    Runs the broked async tasks.

- Beat
    Scheduler for repeating tasks.


.. _packages_overview:

Packages
^^^^^^^^^^^^^^^^

- :ref:`api <api-package>`
    This is the main API providing everything for the primary task: documentation of working time!

- :ref:`faq <faq-package>`
    Package to provide the faq app.

- :ref:`feedback <feedback-package>`
    Package to provide the feedback app.

- :ref:`message <message-package>`
    Package to provide the massage app.

- :ref:`project celery <project-celery-package>`
    Package to provide async working threads on the Calery Worker via the Rabbit Broker.


.. _celery:

Celery
--------------------

The project is using in the backend for most of the task the scheduler Celery for async operations.

Celery is actually only in the local development environment via ``docker compose`` accessible. The reason for that is,
that Clock is developed with the principle to separate the Celery environment and the business envirnoment in two
:ref:`containers <docker-container>`, web container and celer container, and actually (oct 2018) this is not realizable
with Dokku.

To test the Celery in the local development environment, please run the docker containers locally as explained
:ref:`here <local-installation>`. After that visit `localhost <localhost:8000/api/celery-dummy>`_. This will create
5 test user with username ``Tim<rand-int>`` and prints for each new user some logging in stdout.


.. _git_hub:

Git-Hub
--------------------

Clock is versioned with git hub using the
`git-flow <https://www.atlassian.com/de/git/tutorials/comparing-workflows/gitflow-workflow>`_ workflow.
You can find the current stand for backend and frontend `here <https://github.com/ClockGU>`_.


.. _code_format:

Code Format
--------------------
.. note::

    English follows....


Wie bereits am Badge erkenntlich, ist der Code des Projektes durch den Black Formatter formatiert. Die Codeformatierung
wird durch Travis CI in jedem PR überprüft. Erfüllt der committete Code nicht die Ansprüche des Black Styles, scheitert
der Travis Build. Somit ist jeder interessierte Collaborator angehalten, eine einheitliche Codebase (bzgl. des Styles)
beizusteuern.

Wie halte ich den Black Style ein?

Die einfachste Möglichkeit den Black Style einzuhalten ist, gleich so zu coden. Die Richtlinien wie Black Style
aussieht sind hier :ref:`hier <https://github.com/ambv/black#the-black-code-style>` zu finden.

Eine weitere Möglichkeit wäre es, Black jedes mal selbst auszuführen. Dazu muss Black nicht mal systemweit installiert
werden, da das Projekt black automatisch im Pipenv installiert. Um schließlich die Formatierung des gerade
geschriebenen Codes durchzuführen, führt einfach ``docker-compose run --rm web black``. aus. Wem das zu viel getippe ist,
kann auch ``make`` benutzen. Hier stellt das Projekt bereits ein Makefile und zwei Commands bezüglich Black zur Verfügung.
Mit `make black-check` (nicht zu verwechseln mit Black Jack rofl) wird kein Code formatiert, sondern lediglich überprüft
ob und wenn ja wie viele Files von einer Formatierung betroffen wären. Mit ``make black-format`` formatiert man alle, noch
nicht dem Style genügenden, Files.

Eine letzte Möglichkeit ist es, Git-Hooks auszunutzen; den pre-commit Hook. Dieser Hook führt Befehle/Skripte/Programme
aus, bevor Git tatsächlich einen Commit durchführt. Um dies zu tun, ist das Pythonprogramm
:ref:`pre-commit <https://pre-commit.com/>` nötig. Dies kann simpel über ``sudo pip install pre-commit`` installiert
werden. Anschließend muss nur noch der vom Projekt in ``.pre-commit-config.yaml`` definierte Hook installiert werden.
Dies geschieht durch ``pre-commit install``. Nun muss man sich keine Gedanken mehr über Black machen. Bei jedem Commit
wird der Black Formatter über den Code geschickt.

