FROM python:3.9-alpine

WORKDIR /backend

RUN apk add libc-dev
RUN apk add libpq-dev
RUN apk add gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY config.ini .
COPY migrations.yml .

EXPOSE 8000
