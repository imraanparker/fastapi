Overview
========

A sample API application to show off FastAPI

Requirements
============

- `Python 3.8`
- `Docker`
- `Heroku CLI`

Installation
============

Development
------------

Create a virtual environment

```
 python3 -m venv /path/to/env
```

Activate the environment and install the requirements in the app folder

```
/path/to/env/bin/pip install -U -r requirements.txt
```

Run the development web server in the app folder

```
uvicorn main:app --reload
```

Production
----------

A docker container is deployed to Heroku for production use. Run the script to deploy to production.

```
./deploy.sh
```

Accessing the API
------------------

You can access the api via a browser and use the builtin Swagger interface to interact with the API.

When running in development use

```
http://localhost:8000/docs
```

Continuous Integration
=====================

All commits to master runs a test build on Travis CI. ![Last Build](https://travis-ci.com/imraanparker/fastapi.svg?branch=master)

Tests
======

To run the tests locally, simply run

```
pytest
```
