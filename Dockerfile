FROM python:3.6-alpine

COPY ./src /app
WORKDIR /app

RUN apk update \
    && apk add build-base linux-headers
RUN pip install --trusted-host pypi.org  -r requirements.txt

CMD [ "python", "./main.py <BASE_URL> <ROUTE>"]