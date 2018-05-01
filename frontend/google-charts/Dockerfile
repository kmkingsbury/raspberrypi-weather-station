FROM php:7.0-apache
RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get install -y libpq-dev \
    && docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql \
    && docker-php-ext-install pdo_pgsql pgsql
