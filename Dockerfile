FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

COPY main.py ./
COPY src/*.py ./src/
COPY requirements.txt ./

RUN pip install -r requirements.txt 

EXPOSE 8080

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 -timeout 0 main:app
