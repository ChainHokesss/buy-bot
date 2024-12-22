FROM python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update

WORKDIR /code/
COPY Pipfile /code/
COPY Pipfile.lock /code/
COPY entrypoint.sh /code/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy
RUN chmod +x ./entrypoint.sh

COPY . /code/
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
