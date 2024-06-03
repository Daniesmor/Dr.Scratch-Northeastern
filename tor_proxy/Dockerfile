# Usa una imagen base
FROM alpine:latest

LABEL maintainer="daniesmor"

# Install system dependencies
RUN apk update && \
    apk add --no-cache tor && \
    rm -rf /var/cache/apk/


# Configurar Tor
COPY torrc /etc/tor/torrc

# Exponer el puerto de control de Tor
EXPOSE 9050