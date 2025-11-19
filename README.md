# IOr
IO (In &amp; Out) Remastered minimalist files server

### Description
lightweight, minimal dependencies, python based files server with web UI, for easy LAN files sharing.

#### Tech stack:
- `Flask`
- `SQLAlchemy` (+ `alembic` for migrations)
- `whimdb`
- `html`, `css` and some `js`
- `gunicorn`
- `docker`

### Features
- web based UI
- accounts based authentication
- chunked files upload
- configurable user's files storage size
- grouping files into directories
- searching for files & directories
- generating zip files on the fly for downloads
- directories sharing (via link)
- user accessible read-only logs like actions, authentications etc. (cleaned after 28 days)
- support for internationalization (i18n)
- background tasks for files cleanup
- support for HTTPS
- docker based containerization

### Motivation
As with most of my projects, it was about learning, getting a working files server was a nice bonus.

Creating this project (with dependencies limitations in mind) required some extra work, following modules had to be created from scratch:

- csrf protection (`io_csrf`)
- session based authentication
- forms rendering + validation (`io_forms`)
- files chunk based uploader
- generating & streaming zip files on the fly
- page based data pagination
- i18n module (`io_i18n`)
- every icon

### Production Setup
1. Clone this repo

2. Create `.env.docker` file and setup its values:
```
cp .env.docker.template .env.docker
```

3. Create `.env.app` file and setup its values:
```
cp .env.app.template .env.app
```

4. (Optional) Enable HTTPS, generate new certificates, or provide your own
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

5. Run docker container.
```
docker compose --env-file .env.docker build --no-cache
docker compose --env-file .env.docker up -d
```

### Dev Setup
1. Clone this repo
2. Create `.env.app` file
```
cp .env.app.template .env.app
```
3. Change `REDIS_SERVER_ADDRESS` in `.env.app` to `127.0.0.1`
4. Install development dependencies 
```
pip3 install -r requirements/common.txt
pip3 install -r requirements/dev.txt
```
5. Run DEV docker-compose
```
docker compose -f docker-compose-dev.yml up
```
6. Start webserver
```
python3 app.py
```

### Database Migrations
```
python3 migrate.py
```

### Users Management
1. Bash into container
```
docker container exec -it "ior-app" bash
```
2. Run management cli
```
python3 run_management_cli.py
```

### Tests
App contains some example tests for available routes. To run them:
```
pytest -v tests/
```
