FROM python:3-slim-bookworm

# Necessary for psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY manage.py manage.py
COPY config.py config.py
COPY boot.sh boot.sh
RUN chmod a+x boot.sh

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
