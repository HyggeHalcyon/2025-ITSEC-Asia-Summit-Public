#!/bin/bash

exec timeout -sKILL 300 qemu-system-aarch64 \
    -machine virt \
    -m 256 \
    -cpu cortex-a55 \
    -smp cores=1,threads=1 \
    -kernel /home/pwn/Image \
    -initrd /home/pwn/initramfs.cpio.gz \
    -no-reboot \
    -append "console=ttyAMA0 kaslr smep smap kpti=on quiet log_level=3 panic=1 oops=panic" \
    -nographic 