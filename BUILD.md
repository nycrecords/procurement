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
git clone git@github.com:nycrecords/procurement.git
cd procurement
```

Create a virtual environment and install the requirements:
```bash
python3 -m venv procurements
source procurements/bin/activate
pip install -r requirements/dev.txt
```

Now do `flask run` and the server will be running port 5000.

# Docker build
## Development build
```bash
docker-compose up development
```
The server will be open on port 5000.
## Production build
```bash
docker-compose up production
```
The server will be open on port 8080.
