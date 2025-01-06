#!/bin/sh

# Compile translations once during start
python manage.py compilemessages

# Run Django development server to serve static files
python manage.py collectstatic --noinput

while true; do
    echo "Starting Uvicorn ASGI server!"
    uvicorn config.asgi:application --host 0.0.0.0 --port 8000
    sleep 2
done
