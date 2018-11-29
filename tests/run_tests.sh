#!/bin/bash

set -e

COMPOSE_BASE_FILE='tests/docker-compose-base.yml'
COMPOSE_SERVICE_FILE='tests/docker-compose-service.yml'

# Let's brute force the exposed ports. Should be used a cooler solution but it will do for now.
cat docker-compose-base.yml | sed 's|8001:8000|8000:8000|' > "${COMPOSE_BASE_FILE}"

function msg() {
    echo
    echo "======================================="
    echo "  $1"
    echo "======================================="
    echo
}

function finish() {
    msg "Saving the logs"
    docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERVICE_FILE}" logs > logs.txt

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
    --db-port 8000

msg "Staring docker compose"
docker-compose -f "${COMPOSE_BASE_FILE}" -f "${COMPOSE_SERVICE_FILE}" up --build -d

msg "Waiting for health check result"
python check_services.py \
    "http://localhost:5000/health" \
    "http://localhost:5001/health"

msg "Running the tests"
set +e
pytest tests -v
RES=$?

exit ${RES}
