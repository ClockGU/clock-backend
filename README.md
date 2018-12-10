Als Proof-of-Concept dass centry lokal funktioniert :
1. Starte ein Terminal und starte den Dockercontainer via `docker-compose up`
    - Dies startet die Datenbank, den Webserver, einen Rabbit MQ broker und einen celery_worker
2. Starte ein weiteres Terminal und führe `docker-compose run --rm web python -m api.execute_tasks` aus
    - Dies führt die Datei `execute_tasks.py`aus welche lediglich "This Task starts." ausgibt, 20 Sekunden schläft
      und anschließend "This Task ends." ausgibt.
      