Running the Docker Postgresql Image:

```docker run --restart always --name  weatherstation-postgres  -e POSTGRES_USER=weatherstation -e POSTGRES_PASSWORD=weatherstation -e POSTGRES_DB=weatherstation -d postgres -c 'shared_buffers=256MB' -c 'max_connections=200'```

```docker run --restart always --name  weatherstation-postgres -e POSTGRES_PASSWORD_FILE=/run/secrets/postgres-passwd -d postgres```

Get a simple psql shell:

```docker run -it --rm --link weatherstation_psql:postgres postgres psql -h postgres -U postgres```

Use the pgadmin tool to connect to the DB:

```docker run -d -p 5050:5050 chorss/docker-pgadmin4```
http://localhost:5050/browser/

Running the Docker Postgresql Image but with our data / format in it:

```docker build -t weatherstation_psql .
docker run -d --name weatherstation_psql_running -p 5432:5432 weatherstation_psql```
