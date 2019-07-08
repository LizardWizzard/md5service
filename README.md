## MD5 Service

Small MD5 calculation service created for test

### Usage

Best option for testing is as simple as: `docker-compose up`.
Test setup includes `maildev` for simple email interaction checking.

For "production" use specify `ENV` environment variable which
should contain path to valid env configuration file for usage with an application.
Launch with: `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

### Development

For local development use `poetry` and install all dependencies with `poetry install`.
Also for convenient style checking auto reformatting is used with pre-commit hook. 
To install use `pre-commit install` command.
 
To run tests use `pytest`.