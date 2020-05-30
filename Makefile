.PHONY: init ci analyze build rebuild migrate lang-make lang-compile

init:
	poetry install
ci:
	poetry run pytest --cov=./
analyze:
	poetry run flake8 .
	poetry run isort -v
build:
	docker-compose build
rebuild:
	docker-compose build --force-rm --no-cache
migrate:
	docker-compose run --rm web python manage.py migrate
lang-make:
	poetry run python manage.py makemessages --no-location --no-wrap
lang-compile:
	poetry run python manage.py compilemessages
black-check:
	docker-compose run --rm web black . --check
black-format:
	docker-compose run --rm web black .
pytest:
	docker-compose run --rm web pytest
