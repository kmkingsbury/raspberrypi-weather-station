#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER weatherstation;
    CREATE DATABASE weatherstation;
    GRANT ALL PRIVILEGES ON DATABASE weatherstation TO weatherstation;
EOSQL
