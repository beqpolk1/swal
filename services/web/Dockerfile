FROM python:3.12.8-alpine

RUN adduser -D flaskuser

WORKDIR /www/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER flaskuser