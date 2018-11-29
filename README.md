# Testing with docker compose

Trying out how to run tests with using docker-compose to start up 
dependencies and the tested services also.

## Service overview

The service is a Flask-based application which used DynamoDB as a backend.

The local dev server and the tests expose different ports to the host to make
it possible to run them at the same time.

### Local dev server

Use the following command to run the local dev server:

```bash
./run_dev.sh
```

Ports exposed for the host:

 * 8001: local DynamoDB
 * 5002: Flask app

Ports exposed on docker-compose network:

 * local-db:8000
 * dev-server:5000

The source code is mounted to the Flask service to allow automatic code reload
on source code change.

### Test runner

Use the following command to run the tests:

```bash
tests/run_tests.sh
```

Ports exposed for the host:

 * 8000: local DynamoDB
 * 5000: Flask app in "test" mode
 * 5001: Flask app in "production" mode

Ports exposed on docker-compose network:

 * local-db:8000
 * test-server:5000
 * prod-server:5000

### Ports overview

| Service   | Dev  | Test      |
|-----------|------|-----------|
| DynamoDB  | 8001 | 8000      |
| Flask app | 5002 | 5000,5001 |

## Test flow

Running the tests contains the following steps:

  1) Starting up the local DynamoDB service.
  2) Filling the database with data.
  3) Starting up two test services (one in test and one in production mode)
  4) Running the test cases against the services.
  5) Shutting down the services.
