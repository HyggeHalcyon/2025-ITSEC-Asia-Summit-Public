FROM php

USER www-data
WORKDIR /var/www/html

USER root
COPY ./src/index.php .
COPY ./src/ping.php .

USER www-data
EXPOSE 8080
CMD php -S 0.0.0.0:8080
