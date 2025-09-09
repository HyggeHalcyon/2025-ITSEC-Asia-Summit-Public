# This is your client app builder, so you dont wasting time :D
FROM node:22 AS builder

WORKDIR /app

COPY . .

RUN npm install && npm run build:linux

FROM busybox AS artifact

WORKDIR /output

COPY --from=builder /app/release/0.0.0/linux-unpacked ./
