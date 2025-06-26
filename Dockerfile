FROM python:3.9-alpine3.13
LABEL maintainer="nemati.ai"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app

EXPOSE 8000

ARG DEV=false

# Install necessary dependencies for building Python packages
# Install necessary dependencies for building Python packages
RUN python -m venv /py && \
    # Upgrade pip to the latest version
    /py/bin/pip install --upgrade pip && \
    # Install PostgreSQL client and other necessary packages
    apk add --update --no-cache postgresql-client=13.7-r0 jpeg-dev=9.4.0-r0 && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        gcc=10.3.1_git20210424-r2 \
        libc-dev=0.7.2-r3 \
        linux-headers=5.10.41-r0 \
        postgresql-dev=13.7-r0 \
        musl-dev=1.2.2-r3 \
        zlib=1.2.11-r3 \
        zlib-dev=1.2.11-r3 \
        build-base=0.5-r2 && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = true ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Clean up unnecessary files to reduce image size
    rm -rf /tmp && \
    # Remove build dependencies to keep the image size smaller
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add virtual environment to PATH
ENV PATH="/py/bin:$PATH"

# Switch to the non-root user for security
USER django-user
