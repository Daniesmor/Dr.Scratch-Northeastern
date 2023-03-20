FROM python:3.10

LABEL maintainer="cdchushig"

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /var/www
WORKDIR /var/www
ADD . /var/www/

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get autoclean

RUN apt-get install -y \
    default-libmysqlclient-dev \
    texlive-latex-recommended \
    gettext

# RUN apt-get install python3.10-dev

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /var/www/app/certificate

EXPOSE 8000
