FROM python:3.9-alpine

WORKDIR /transfers

RUN apk add libc-dev
RUN apk add libpq-dev
RUN apk add gcc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY config.ini .

EXPOSE 8000
