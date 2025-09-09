FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install qemu-system-arm qemu-efi-aarch64 qemu-utils 
RUN apt-get -y install xinetd hashcash
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD --chmod=640 ./pwn.xinetd /etc/xinetd.d/pwn
ADD --chmod=700 ./init.sh /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
ADD --chmod=550 ./pow.sh pow.sh
ADD ./app .
RUN chmod a+x run.sh

RUN chown -R root:pwn /home/pwn
RUN chmod -R go-w /home/pwn

