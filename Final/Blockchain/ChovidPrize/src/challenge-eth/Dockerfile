FROM dimasmaualana/eth:latest

COPY deploy/ /home/ctf/

COPY contracts /tmp/contracts

RUN true \
    && cd /tmp \
    && forge build --out /home/ctf/compiled \
    && forge build --evm-version prague --out /home/ctf/compiled \
    && rm -rf /tmp/contracts \
    && true
