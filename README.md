# HVV Case Study for Infrastructure and Lot 2
## Lot 2: Backend

## Getting started
1. Clone this repository
1. Build the image
    ```bash
    $ docker build -t hvv-case-studt -f ./images/base/Dockerfile .
    ```
1. Run the image
    ```bash
    $ docker run -p 5000:5000 hvv-case-study
    ```
1. Access the API on `localhost:5000`

### Infrastructure

* The `dev` branch is the default branch/trunk for this source code.
* Implementations of two endpoints for gathering statistics have been created.
* A small sample test suite has been created for showcasing a future test-flow.
* Two Github Actions have been created:
  * (*Immediate Feedback*) On open and sync for any PR targeting `dev`:
    * runs formatting using [ruff](https://docs.astral.sh/ruff/), if successful
    * runs a sample test suite of the application.
  * (*Deploying*) On push to `dev`(*) a CI/CD pipeline will:
    * runs a sample test suite of the application, if successful
    * builds the application using [Docker](https://www.docker.com) and push it to a [Github Container registry](https://github.com/kineo-ai/hvv-case-study/pkgs/container/hvv-case-study).

### Authentication
For self-managed authentication, [Keycloak](https://github.com/keycloak/keycloak) could be used. It allows for user management out-of-the-box, service-to-service communication as well as OAuth-flows. This solution is readily extensible and gives Administrators and Operators control over the whole authentication process.

An alternative is to use a managed authentication provider, through a cloud operator of choice, for instance [Amazon Cognito](https://aws.amazon.com/cognito/) or [Azure AD B2C](https://azure.microsoft.com/en-us/products/active-directory-b2c/). In this case managing users/clients can be implemented using OAuth-flows through their preferred authentication provider without the need for managing each provider manually.

### Discussion & Future Improvements

* To use a production-level solution for [Flask](https://flask.palletsprojects.com/en/3.0.x/deploying/) and create TLS certificates for hosting the application.
* Pre-emptive input validation on Endpoints: At the moment we are not prohibiting the input for country names before we have received the input. The reason for this is primarily the lack of requirements for the integration with downstream services (e.g. Lot 1: Frontend), users or SDKs. Possible options could be:
  * Pre-processing and validating inputs to prohibit malicious attempts before using it.
  * Use the Content-Type `application/json` to give users the ability to send data that does not have to be URL encoded (e.g. not having to use %20).
  * Providing users with a list/options of valid inputs (e.g. Dropdown of country names).
* Automatic Documentation Generation: By using modules such as [pydoc](https://docs.python.org/3/library/pydoc.html) and [Sphinx](https://github.com/sphinx-doc/sphinx) we would be able to generate canonical documentation for SDK and API reference.

> (*) This is equivalent behaviour to `on merge of PR of branch targeting dev`