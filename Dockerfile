FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app

WORKDIR /app/app

RUN pip install -U -r requirements.txt
