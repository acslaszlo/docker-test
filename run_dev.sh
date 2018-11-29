#!/bin/bash

set -e

COMPOSE_BASE_FILE='docker-compose-base.yml'
COMPOSE_SERVICE_FILE='docker-compose-dev.yml'

function msg() {
    echo
    echo "======================================="
    echo "  $1"
    echo "======================================="
    echo
}

function finish() {
    msg "Stopping docker compose"
    docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERVICE_FILE}" down
}

trap finish EXIT

. test-venv/bin/activate
pip install -r tests/requirements.txt

msg "Starting local db"
docker-compose -f "${COMPOSE_BASE_FILE}" up --build -d

msg "Initializing the db"
PYTHONPATH=. \
    python tests/init_db.py \
    --db-port 8001

msg "Staring docker compose"
docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERVICE_FILE}" up --build
