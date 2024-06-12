# Usa una imagen base
FROM python:3.10

LABEL maintainer="cdchushig"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /var/www

# Añadir la aplicación al contenedor
ADD . /var/www/

# Actualizar pip e instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Asignar permisos de ejecución
RUN chmod +x /var/www/app/certificate

# Exponer el puerto de la aplicación
EXPOSE 8000
