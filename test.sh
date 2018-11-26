#!/bin/bash

set -e

COMPOSE_BASE_FILE='docker-compose-base.yml'
COMPOSE_SERICE_FILE='tests/docker-compose-service.yml'

function msg() {
    echo
    echo "======================================="
    echo "  $1"
    echo "======================================="
    echo
}

function finish() {
    msg "Saving the logs"
    docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERICE_FILE}" logs > logs.txt

    msg "Stopping docker compose"
    docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERICE_FILE}" down
}

trap finish EXIT

. test-venv/bin/activate
pip install -r tests/requirements.txt

msg "Starting local db"
docker-compose -f "${COMPOSE_BASE_FILE}" up --build -d

msg "Initializing the db"
python tests/init_db.py

msg "Staring docker compose"
docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERICE_FILE}" up --build -d

msg "Waiting for health check result"
python check_services.py \
    "http://localhost:5000/health" \
    "http://localhost:5001/health"

msg "Running the tests"
set +e
pytest tests -v
RES=$?

exit ${RES}
