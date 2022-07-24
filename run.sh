#!/bin/sh

# shellcheck disable=SC2039
source venv/bin/activate

while true; do
    flask deploy
    # shellcheck disable=SC2181
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - application:app
