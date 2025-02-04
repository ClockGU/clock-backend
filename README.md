![Clock Logo](https://raw.githubusercontent.com/ClockGU/documentation/master/images/clock_current_logo_600x150.png)

<h2 align="center"> Arbeitszeitdoukumentation einfach EINFACH </h2>

<p align="center">
<a href="https://travis-ci.org/ClockGU/clock-backend"><img alt="Build Status" src="https://travis-ci.org/ClockGU/clock-backend.svg?branch=master"></a>
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://codecov.io/github/ClockGU/clock-backend?branch=master"><img alt="Coverage" src="https://codecov.io/github/ClockGU/clock-backend/coverage.svg?branch=master"></a>
<a href="https://clock-backend.readthedocs.io/en/latest/index.html#"><img alt="docs: in progress" src="https://img.shields.io/static/v1?label=docs&message=in%20progress&color=yellow"></a>
</p>


## Development

### Code Format

Wie bereits am Badge erkenntlich, ist der Code des Projektes durch den Black Formatter formatiert. Die Codeformatierung
wird durch Travis CI in jedem PR überprüft. Erfüllt der committete Code nicht die Ansprüche des Black Styles, scheitert
der Travis Build. Somit ist jeder interessierte Collaborator angehalten, eine einheitliche Codebase (bzgl. des Styles) 
beizusteuern.

Wie halte ich den Black Style ein?

Die einfachste Möglichkeit den Black Style einzuhalten ist, gleich so zu coden. Die Richtlinien wie Black Style aussieht
sind [hier](https://github.com/ambv/black#the-black-code-style) zu finden.

Eine weitere Möglichkeit wäre es, Black jedes mal selbst auszuführen. Dazu muss Black nicht mal systemweit installiert
werden, da das Projekt black automatisch im Pipenv installiert. Um schließlich die Formatierung des gerade geschriebenen
Codes durchzuführen, führt einfach `docker-compose run --rm web black .` aus. Wem das zu viel getippe ist, kann auch 
`make` benutzen. Hier stellt das Projekt bereits ein Makefile und zwei Commands bezüglich Black zur Verfügung.
Mit `make black-check` (nicht zu verwechseln mit Black Jack :rofl:) wird kein Code formatiert, sondern lediglich
überprüft ob und wenn ja wie viele Files von einer Formatierung betroffen wären. Mit `make black-format` formatiert man
alle, noch nicht dem Style genügenden, Files.

Eine letzte Möglichkeit ist es, Git-Hooks auszunutzen; den pre-commit Hook. Dieser Hook führt Befehle/Skripte/Programme
aus, bevor Git tatsächlich einen Commit durchführt. Um dies zu tun, ist das Pythonprogramm [pre-commit](https://pre-commit.com/)
nötig. Dies kann simpel über `sudo pip install pre-commit` installiert werden. Anschließend muss nur noch der vom Projekt
in `.pre-commit-config.yaml` definierte Hook installiert werden. Dies geschieht durch `pre-commit install`. Nun muss man
sich keine Gedanken mehr über Black machen. Bei jedem Commit wird der Black Formatter über den Code geschickt.


## Celery

Das Projekt Clock nutzt im Backend für diverse Aufgaben Celery, um diese asynchron abzuwickeln.

Bis jetzt (**Stand Dez. 2018**) ist Celery nur in der lokalen Entwicklungsumgebung durch `docker-compose`
zugänglich. Der Grund hierfür ist, dass das von uns verfolgte Prinzip "Celeryumgebung abgekoppelt von Bussinesumgebung",
also zwei Container, Web-Container und Celery-Container, noch (**Stand Okt. 2018**) nicht auf Dokku übertragbar ist.

In der Developmentumgebung existiert eine funktionierende Implementation, die im Folgenden erläutert wird.

Als Proof-of-Concept, dass Celery lokal funktioniert :
1. Starte ein Terminal und starte den Dockercontainer via `docker-compose up`
    - Dies startet die Datenbank, den Webserver, einen Rabbit MQ broker und einen celery_worker
    - sind mehr als ein Worker erwünscht, so muss folgender Command zum Starten benutzt werden `docker-compose up --scale celery_worker=N` für *N* Worker.
2. Um die Funktionalität zu prüfen, öffne einen Browser der Wahl
3. Wähle die url `localhost:8000/api/celery-dummy` an
    - Diese View erstellt asynchron 5 User mit Username `Tim<rand-int>`
    - Ferner printet sie vor jedem Erstellen und danach jeweils etwas in stdout.
Query um alle Contracts zu bekommen die in einem bestimmten Monat (hier Oktober 2024) gelocked sind
existing_shifts = Shift.objects.filter(started__date__gte=nov, started__date__lte=date(2024,10,31), locked=True, contract=OuterRef("pk"))
oct_locked_contracts = Contract.objects.filter(Exists(existing_shifts))
 Andere Methode:
Shift.objects.filter(started__date__gte=october, started__date__lte=date(2024,10,31), locked=True).values("contract").distinct()


      