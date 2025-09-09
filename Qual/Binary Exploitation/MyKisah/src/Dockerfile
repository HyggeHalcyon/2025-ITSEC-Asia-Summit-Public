FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && \
    apt-get install -y socat build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -u 1000 -d /home/user -s /bin/bash user

WORKDIR /home/user

COPY chall.c /home/user/
COPY build.sh /home/user/
COPY flag.txt /home/user/

RUN ./build.sh
RUN rm /home/user/build.sh
RUN rm /home/user/chall.c
RUN chmod 111 /home/user/MyKisah
RUN chmod 444 /home/user/flag.txt
RUN chmod -R 555 /home/user

EXPOSE 1337
ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork,nodelay,su=user", "EXEC:'timeout 180 ./MyKisah'"]
