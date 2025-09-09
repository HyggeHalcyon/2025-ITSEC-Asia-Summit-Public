# Dockerfile
FROM python:3.9-slim

RUN groupadd -r ctfgroup && useradd -r -g ctfgroup ctf

WORKDIR /app

COPY . .

RUN chown -R ctf:ctfgroup /app
RUN chmod -R 555 /app

USER ctf

EXPOSE 14437

CMD ["python", "verify.py"]
