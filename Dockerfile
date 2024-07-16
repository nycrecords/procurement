# ================================= PRODUCTION =================================
FROM python:3-slim-bookworm AS production

# Necessary for psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements/prod.txt ./requirements/
RUN pip install -r requirements/prod.txt
RUN pip install gunicorn

COPY app ./app/
COPY migrations ./migrations/
COPY manage.py config.py entrypoint.sh gunicorn-conf.py ./

RUN chmod +x entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "-c", "python:gunicorn-conf", "manage:app"]

# ================================= DEVELOPMENT ================================
FROM python:3-slim-bookworm AS development

COPY requirements/dev.txt ./requirements/
RUN pip install -r requirements/dev.txt
COPY app ./app/
COPY migrations ./migrations/
COPY manage.py config.py ./

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
