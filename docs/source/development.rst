development
===============


.. toctree::
   :maxdepth: 4

   development


Code Format
----------

Wie bereits am Badge erkenntlich, ist der Code des Projektes durch den Black Formatter formatiert. Die Codeformatierung wird durch Travis CI in jedem PR überprüft. Erfüllt der committete Code nicht die Ansprüche des Black Styles, scheitert der Travis Build. Somit ist jeder interessierte Collaborator angehalten, eine einheitliche Codebase (bzgl. des Styles) beizusteuern.

Wie halte ich den Black Style ein?

Die einfachste Möglichkeit den Black Style einzuhalten ist, gleich so zu coden. Die Richtlinien wie Black Style aussieht sind hier zu finden.

Eine weitere Möglichkeit wäre es, Black jedes mal selbst auszuführen. Dazu muss Black nicht mal systemweit installiert werden, da das Projekt black automatisch im Pipenv installiert. Um schließlich die Formatierung des gerade geschriebenen Codes durchzuführen, führt einfach docker-compose run --rm web black . aus. Wem das zu viel getippe ist, kann auch make benutzen. Hier stellt das Projekt bereits ein Makefile und zwei Commands bezüglich Black zur Verfügung. Mit make black-check (nicht zu verwechseln mit Black Jack rofl) wird kein Code formatiert, sondern lediglich überprüft ob und wenn ja wie viele Files von einer Formatierung betroffen wären. Mit make black-format formatiert man alle, noch nicht dem Style genügenden, Files.

Eine letzte Möglichkeit ist es, Git-Hooks auszunutzen; den pre-commit Hook. Dieser Hook führt Befehle/Skripte/Programme aus, bevor Git tatsächlich einen Commit durchführt. Um dies zu tun, ist das Pythonprogramm pre-commit nötig. Dies kann simpel über sudo pip install pre-commit installiert werden. Anschließend muss nur noch der vom Projekt in .pre-commit-config.yaml definierte Hook installiert werden. Dies geschieht durch pre-commit install. Nun muss man sich keine Gedanken mehr über Black machen. Bei jedem Commit wird der Black Formatter über den Code geschickt.

Celery
----------

Das Projekt Clock nutzt im Backend für diverse Aufgaben Celery, um diese asynchron abzuwickeln.

Bis jetzt (Stand Dez. 2018) ist Celery nur in der lokalen Entwicklungsumgebung durch docker-compose zugänglich. Der Grund hierfür ist, dass das von uns verfolgte Prinzip "Celeryumgebung abgekoppelt von Bussinesumgebung", also zwei Container, Web-Container und Celery-Container, noch (Stand Okt. 2018) nicht auf Dokku übertragbar ist.

In der Developmentumgebung existiert eine funktionierende Implementation, die im Folgenden erläutert wird.

Als Proof-of-Concept, dass Celery lokal funktioniert :

* Starte ein Terminal und starte den Dockercontainer via docker-compose up
        Dies startet die Datenbank, den Webserver, einen Rabbit MQ broker und einen celery_worker
        sind mehr als ein Worker erwünscht, so muss folgender Command zum Starten benutzt werden docker-compose up --scale celery_worker=N für N Worker.
* Um die Funktionalität zu prüfen, öffne einen Browser der Wahl
* Wähle die url localhost:8000/api/celery-dummy an
        Diese View erstellt asynchron 5 User mit Username Tim<random-int>
        Ferner printet sie vor jedem Erstellen und danach jeweils etwas in stdout.

