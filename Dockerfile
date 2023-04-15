FROM python:3.10

COPY requirements.txt database.db ./
COPY app app

RUN pip install -r requirements.txt

WORKDIR app