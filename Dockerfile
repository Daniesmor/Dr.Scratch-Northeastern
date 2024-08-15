# Usa una imagen base
FROM python:3.10

LABEL maintainer="cdchushig"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gettext \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js y npm
RUN apt update -y && apt install nodejs npm -y

# Establece el directorio de trabajo
WORKDIR /var/www

# Añadir la aplicación al contenedor
ADD . /var/www/

# Actualizar pip e instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install npm dependencies
COPY package.json ./
RUN npm install

# Asignar permisos de ejecución
RUN chmod +x /var/www/app/certificate

# Exponer el puerto de la aplicación
EXPOSE 8000
