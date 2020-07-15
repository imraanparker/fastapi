FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

WORKDIR /app

RUN pip install -U -r requirements.txt
