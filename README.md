![Clock Logo](https://raw.githubusercontent.com/ClockGU/documentation/master/images/clock_current_logo_600x150.png)

<h2 align="center"> Arbeitszeitdoukumentation einfach EINFACH </h2>

<p align="center">
<a href="https://travis-ci.org/ClockGU/clock-backend"><img alt="Build Status" src="https://travis-ci.org/ClockGU/clock-backend.svg?branch=master"></a>
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://codecov.io/github/ClockGU/clock-backend?branch=master"><img alt="Coverage" src="https://codecov.io/github/ClockGU/clock-backend/coverage.svg?branch=master"></a>
</p>


## Celery

Das Projekt Clock nutzt im Backend für diverse Aufgaben Celery um diese asynchron abzuwickeln.

Bis jetzt (**Stand Dez. 2018**) ist Celery nur in der lokalen Entwicklungsumgebung durch `docker-compose`
zugänglich. Der Grund hierfür ist, dass das von uns verfolgte Prinzip "Celeryumgebung abgekoppelt von Bussinesumgebung"
also zwei Container, Web-Container und Celery-Container, noch (**Stand Okt. 2018**) nicht auf Dokku übertragbar ist.

In der Developmentumgebung existiert eine funktionierende Implementation welche im Folgenden erläutert wird.

Als Proof-of-Concept dass centry lokal funktioniert :
1. Starte ein Terminal und starte den Dockercontainer via `docker-compose up`
    - Dies startet die Datenbank, den Webserver, einen Rabbit MQ broker und einen celery_worker
    - sind mehr als ein worker erwünscht so muss folgender Command zum starten benutzt werden `docker-compose up --scale celery_worker=N` für *N* worker.
2. Um die Funktionalität zu prüfen öffne einen Browser der Wahl
3. Wähle die url `localhost:8000/api/celery-dummy` an
    - Diese View erstellt asynchron 5 User mit Username `Tim<rand-int>`
    - Ferner printet sie vor jedem erstellen und danach jeweils etwas in stdout.


      