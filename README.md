# Testing with docker compose

Trying out how to run tests with using docker-compose to start up 
dependencies and the tested services also.

## Service overview

The service is a Flask-based application which used DynamoDB as a backend.

## Test flow

Running the tests contains the following steps:

  1) Starting up the local DynamoDB service.
  2) Filling the database with data.
  3) Starting up two test services (one in test and one in production mode)
  4) Running the test cases against the services.
  5) Shutting down the services.
