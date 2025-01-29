FROM python:3.10

LABEL maintainer="cdchushig"

# Set Python environment variables

RUN apt-get update && apt-get install -y \
    gettext \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www

ADD . /var/www/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /var/www/app/certificate

EXPOSE 8000
