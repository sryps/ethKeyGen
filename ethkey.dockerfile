FROM rust:1.71.0-bookworm AS build-env-rust
WORKDIR /root
RUN git clone https://github.com/sryps/eth-staking-smith.git
RUN cd eth-staking-smith && cargo build --release


FROM golang:1.20-bullseye AS build-env-go
WORKDIR /root
RUN export prysm_version=$(curl -f -s https://prysmaticlabs.com/releases/latest) && export file_validator=validator-${prysm_version}-linux-amd64 && curl -f -L "https://prysmaticlabs.com/releases/${file_validator}" -o validator
RUN chmod +x validator


FROM python:3.12.0-slim-bookworm
RUN useradd -m eth -s /bin/bash
WORKDIR /home/eth
USER eth:eth
COPY --chown=0:0 --from=build-env-rust /root/eth-staking-smith/target/release/eth-staking-smith /usr/bin/eth-staking-smith
COPY --chown=0:0 --from=build-env-go /root/validator /usr/local/bin/validator
COPY ./ /home/eth/
RUN mkdir -p /home/eth/.eth2validators/prysm-wallet-v2/direct/accounts
RUN mkdir -p /home/eth/keys/validator_keys
RUN pip install flask cryptography requests

CMD [ "python3", "/home/eth/main.py"]