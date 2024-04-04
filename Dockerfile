FROM python:3.11.9-alpine3.19
LABEL maintainer="subham73"

# Set environment variables
ENV PYTHONUNBUFFERED 1
#set to 1 to avoid buffering outputs

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements_dev.txt /tmp/requirements_dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements_dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

#till above, the root user is acting
USER django-user