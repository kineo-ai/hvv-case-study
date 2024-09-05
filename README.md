# HVV Case Study for Infrastructure and Lot 2

## Infrastructure

* dev branch
* CI/CD pipeline that runs after merge of a PR the tests on dev
    * if it succeeds build the application and push it to a container registry (github packages)

Rough concept: 

Minimum: Github Actions for CI/CD stuff

## Lot 2: Backend

### Authentification
Authentification is done via keycloak. In order to start the keycloak service. Copy the `example_env` file and rename it to `.env`. 
Then in a terminal run: `docker compose up --build`.
You can access the UI via `http://localhost:8080/admin/master/console/`