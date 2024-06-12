# Usa una imagen base
FROM alpine:latest

LABEL maintainer="daniesmor"

# Install system dependencies
RUN apk update && \
    apk add --no-cache tor && \
    rm -rf /var/cache/apk/


# Setting up Tor
COPY torrc /etc/tor/torrc

# Expose Tor (listen) port
EXPOSE 9050