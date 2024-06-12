# Usa una imagen base
FROM python:3.10

LABEL maintainer="cdchushig"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema
RUN apt-get update 


# Instalar dependencias de Python
WORKDIR /var/www
ADD . /var/www/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /var/www/app/certificate

# Exponer el puerto de la aplicación
EXPOSE 8000

