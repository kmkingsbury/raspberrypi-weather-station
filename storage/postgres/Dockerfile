# Dockerfile
FROM postgres:latest


COPY structure.sql /docker-entrypoint-initdb.d/
COPY init_docker_postgres.sh /docker-entrypoint-initdb.d/
