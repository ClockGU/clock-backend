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


## Periodische Tasks

Das Projekt beinhaltet zwei periodische Tasks:

1. Monatliche Erstellung von Reports (`manage.py create_reports_monthly`)
2. Deprovisionierung von Nutzer die im Identity Provider (IDM GU) bereits zur Löschung
markiert wurden (`manage.py deprovision_users_monthly`)

 
Die Cron jobs laufen nur in den `production` apps. In den Staging apps sind die cronjobs ausgeschaltet 
via `dokku cron:set <app-staging> maintenance true`. 

Beide Tasks werden nur im staging/production Systems durch "Scheduled Cron Tasks" von `dokku` ausgeführt
und verwaltet.
Die Tasks werden im lokalen Setup nicht ausgeführt.

      