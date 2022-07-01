FROM docker-mirror-io.dcube.devmail.ru/python:3.10-slim

COPY . /metrics
WORKDIR /metrics

ARG VERSION
ARG APP
ARG BUILD_NUMBER
ENV VERSION ${VERSION}
ENV APP ${APP}
ENV BUILD_NUMBER ${BUILD_NUMBER}
ADD requirements.txt requirements.txt
CMD [ "python", "main.py"]

RUN pip install -r requirements.txt

EXPOSE 8080

