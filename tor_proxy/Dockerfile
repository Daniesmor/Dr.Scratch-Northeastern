# Usa una imagen base
FROM python:3.10

LABEL maintainer="daniesmor"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y tor

# Configurar Tor
COPY torrc /etc/tor/torrc

# Instalar dependencias de Python
WORKDIR /var/www
ADD . /var/www/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de control de Tor
EXPOSE 9050