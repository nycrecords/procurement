# ================================= PRODUCTION =================================
FROM python:3-slim-bookworm AS production

# Necessary for psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements/prod.txt requirements/prod.txt
RUN pip install -r requirements/prod.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY manage.py manage.py
COPY config.py config.py
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]

# TODO: Investigate why it gives errors with the "-c" switch
CMD ["gunicorn", "-b", ":5000", "manage:app"]

# ================================= DEVELOPMENT ================================
FROM python:3-slim-bookworm AS development

COPY requirements/dev.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt
COPY app app
COPY migrations migrations
COPY manage.py manage.py
COPY config.py config.py

EXPOSE 5000
CMD ["flask", "run"]
