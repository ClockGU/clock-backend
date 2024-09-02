FROM python:3.10-slim
ARG DJANGO_SETTINGS_MODULE
ARG DJANGO_ADMIN_URL
ARG DJANGO_SECRET_KEY
ARG DATABASE_URL
ARG DJANGO_SENTRY_DSN
ENV PYTHONBUFFERED=1 DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} DJANGO_ADMIN_URL=${DJANGO_ADMIN_URL} DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY} DATABASE_URL=${DATABASE_URL} DJANGO_SENTRY_DSN=${DJANGO_SENTRY_DSN} POETRY_VERSION=1.3.2 POETRY_VIRTUALENVS_CREATE=false

# Add new user to run the whole thing as non-root
RUN groupadd app --gid 32767
RUN adduser --ingroup app --home /app --uid 32767 --disabled-password --gecos "" app

# Install build dependencies
RUN apt update \
    && apt install -y gettext git wkhtmltopdf binutils ca-certificates

# Patch libQt5Core to make wkhmtltopdf work
# See: https://github.com/wkhtmltopdf/wkhtmltopdf/issues/4497#issuecomment-541370182
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

# Set the correct timezone
RUN cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && echo "Europe/Berlin" > /etc/timezone

# Copy pyproject.toml, poetry.lock and install python dependencies
COPY --chown=app:app pyproject.toml poetry.lock /
RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org  | python3 -
RUN PATH="$PATH:$HOME/.local/bin" && poetry install

# Copy dokku specific files to the project root
COPY --chown=app:app docker/dokku/* /app/
COPY --chown=app:app docker/dokku/entrypoint.sh /
RUN chmod +x entrypoint.sh /app/deploy.sh

USER app
WORKDIR /app

# Copy all related app files
COPY --chown=app:app . /app

ENTRYPOINT ["/entrypoint.sh"]
