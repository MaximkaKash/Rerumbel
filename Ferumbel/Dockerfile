FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /Ferumbel

RUN apt-get update && apt update

COPY requirements.txt /Ferumbel

RUN pip install --default-timeout=100 -r requirements.txt