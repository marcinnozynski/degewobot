FROM python:3.10

COPY requirements.txt degewobot/
WORKDIR degewobot

COPY app app

RUN pip install -r requirements.txt

WORKDIR app