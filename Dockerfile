FROM python:3.10.7-slim-buster AS base

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN groupadd ticket_bot
RUN useradd -g ticket_bot ticket_bot
RUN chown -R ticket_bot:ticket_bot /app

RUN apt-get update && apt-get install -y git gcc python3-dev musl-dev libpq-dev cmake build-essential

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt
