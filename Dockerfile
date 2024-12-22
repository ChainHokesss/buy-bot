FROM python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER root

RUN apt-get update

WORKDIR /code/
COPY Pipfile /code/
COPY Pipfile.lock /code/
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY . /code/
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
