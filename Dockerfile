# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster

WORKDIR /simplescraper

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD [ "simplescraper/tests_run.py" ]