FROM python:3.12-alpine

LABEL maintainer="developer@example.com"
LABEL version="1.0"
LABEL description="Videoflix Backend"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk update && \
    apk add --no-cache --upgrade bash && \
    apk add --no-cache postgresql-client ffmpeg py3-redis && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY . .

RUN chmod +x backend.entrypoint.sh

EXPOSE 8000
