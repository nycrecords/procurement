# Build instructions
### Prerequisites
The following dependencies are required:
- [PostgreSQL](https://www.postgresql.org/)
- [libpq](https://www.postgresql.org/docs/9.5/libpq.html)

Make sure you follow `.env.example` to set environment variables for
the application to connect to the database.

# Local Build
Clone the git repository and make it your current directory:
```bash
git clone git@gitlab.com:nycrecords/doris_procurements.git
cd doris_procurements
```

Create a virtual environment and install the requirements:
```bash
python3 -m venv procurements
source procurements/bin/activate
pip install -r requirements.txt
```

Now do `flask run` and the server should be running port 5000.

# Docker build
To run with docker, run
```bash
docker-compose up
```
And the server will be open on port 8080.
