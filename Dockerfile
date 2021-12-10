FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /application
ADD . /application/
WORKDIR /application
RUN apk update \
    && apk add --no-cache --virtual .build-deps build-base linux-headers gcc musl-dev libjpeg-turbo libpng-dev libjpeg-turbo-dev libxml2-dev libxslt-dev postgresql-dev && \
    pip install -r requirements.txt
WORKDIR /application/ocean_freight/
ENV ENVIRONMENT=local
CMD ["python", "manage.py", "runserver", "0.0.0.0:4000"]