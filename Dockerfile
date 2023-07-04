FROM python:3.9-slim

WORKDIR /app

ADD src/logs_parser.py ./src/logs_parser.py
