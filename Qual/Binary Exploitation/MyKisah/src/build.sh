#!/bin/bash
gcc chall.c -o MyKisah \
    -fstack-protector-all \
    -Wl,-z,relro,-z,now,-z,noexecstack
