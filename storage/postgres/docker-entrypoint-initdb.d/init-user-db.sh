#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER weather;
    CREATE DATABASE weather;
    GRANT ALL PRIVILEGES ON DATABASE weather TO weather;
EOSQL
