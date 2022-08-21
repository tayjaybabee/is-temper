# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y python3 python3-pip pkg-config python3-matplotlib python3-pkgconfig

RUN pip3 install --upgrade pip

RUN pip3 install poetry

RUN poetry install

CMD ["python3", "main.py"]
