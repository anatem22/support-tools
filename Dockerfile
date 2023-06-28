FROM artifactory.gitlab.bcs.ru/docker-hub/python:3.8-alpine
ARG HTTPS_PROXY=$HTTPS_PROXY
ARG HTTP_PROXY=$HTTPS_PROXY


WORKDIR /usr/src/app

COPY *.py requirements.txt .

RUN HTTP_PROXY=$HTTPS_PROXY HTTPS_PROXY=$HTTPS_PROXY apk --no-cache add curl tzdata gcc libc6-compat musl-dev libffi-dev libssl1.1 openssl-dev g++ libpq-dev python3-dev
RUN HTTPS_PROXY=$HTTPS_PROXY pip install --no-cache-dir --upgrade pip
RUN HTTPS_PROXY=$HTTPS_PROXY pip install --no-cache-dir -r requirements.txt

#RUN mkdir pg_config
COPY templates templates/

#COPY static static/

RUN chmod a+x *.py
#USER 1001

CMD ["./app.py"]
