# IOr
IO (In &amp; Out) Remastered minimalist files server

#### .env files

```
cp .env.app.template .env.app
cp .env.docker.template .env.docker
```

#### build docker image

```
docker compose --env-file .env.docker build --no-cache
```

#### start app

```
docker compose --env-file .env.docker up -d
```

#### bash into running app container

```
docker exec -it "ior-app" bash
```

#### delete docker containers

```
docker compose --env-file .env.docker down -v
```

#### HTTPS

```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

#### Tests

```
pytest -v tests/
```
