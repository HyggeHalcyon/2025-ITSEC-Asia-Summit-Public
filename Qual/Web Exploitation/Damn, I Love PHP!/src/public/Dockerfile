FROM php:8.2-cli

RUN docker-php-ext-install pdo

WORKDIR /app

RUN mkdir ./data
COPY public/ ./public/
COPY includes/ ./includes/

WORKDIR /app/public

CMD ["php", "-S", "0.0.0.0:8081"]
