FROM node:20-alpine

RUN apk add --no-cache docker-cli

COPY ./bot /bot
RUN mkdir /www
COPY ./www/package.json ./www/yarn.lock /www
WORKDIR /www
RUN yarn
COPY ./www /www

ENTRYPOINT ["/www/run.sh"]
