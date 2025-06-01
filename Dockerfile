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
RUN python -m venv /py && \
    # Upgrade pip to the latest version
    /py/bin/pip install --upgrade pip && \
    # Install PostgreSQL client and other necessary packages
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev build-base && \
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
