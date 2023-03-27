FROM node:10.16.1-alpine

LABEL maintainer="cdchushig"

RUN apk update && apk add --no-cache git
RUN apk add --no-cache openssh

WORKDIR /data
RUN git clone https://github.com/cdchushig/getsb3.git /data/app
WORKDIR /data/app

RUN npm install && npm run build

EXPOSE 3030

CMD ["npm", "start"]