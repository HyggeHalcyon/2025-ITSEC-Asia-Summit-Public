FROM node:22-bookworm-slim

WORKDIR /app
COPY ./package.json ./package-lock.json /app
RUN npm install
COPY . /app

RUN addgroup ctf && \
adduser --disabled-password --gecos "" --ingroup ctf ctf

EXPOSE 5599

CMD ["npm", "run", "start"]
