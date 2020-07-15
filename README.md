Overview
========

A sample API application to show off FastAPI

Requirements
============

- `Python 3.8`_
- `Docker`_
- `Python Date Utilities`_
- `PyTest`_

Running
========

Development
------------

Create a virtual environment

- `python3 -m venv /path/to/env`

Activate the environment and install the requirements in the app folder

- `/path/to/env/bin/pip install -U -r requirements.txt`

Run the development web server in the app folder

- `uvicorn main:app --reload`

Production
----------

Use docker to create a production image for deployment. You can choose any

Tests
======

To run the tests, simply run

- `pytest`

License
=======

Free to use.