# Set default values for build arguments
ARG DEFRA_VERSION=2.0.0
ARG BASE_VERSION=3.13.9-slim-trixie
ARG PYTHON_VERSION=3.13.9

FROM python:${BASE_VERSION} AS production

ARG DEFRA_VERSION
ARG BASE_VERSION

ENV PATH="/home/nonroot/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=production

# Ensure uv is using the Python interpreter from the base image
ENV UV_PYTHON=${PYTHON_VERSION}
ENV UV_MANAGED_PYTHON=0
ENV UV_PYTHON_DOWNLOADS=0

LABEL uk.gov.defra.python.python-version=$BASE_VERSION \
    uk.gov.defra.python.version=$DEFRA_VERSION \
    uk.gov.defra.python.repository=defradigital/python

RUN apt update \
    && apt install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Internal CA certificate for firewall and Zscaler proxy
COPY certificates/internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt
RUN chmod 644 /usr/local/share/ca-certificates/internal-ca.crt && update-ca-certificates

# Create a non-root user for running Python applications
RUN addgroup --gid 1000 nonroot \
    && adduser nonroot \
        --uid 1000 \
        --gid 1000 \
        --home /home/nonroot \
        --shell /bin/bash

# Ensure pip is at latest version
RUN python -m pip install --upgrade pip --force-reinstall

USER nonroot

WORKDIR /home/nonroot

ENTRYPOINT [ "python" ]

FROM production AS development

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=development

# Ensure uv is using the Python interpreter from the base image
ENV UV_PYTHON=${PYTHON_VERSION}
ENV UV_MANAGED_PYTHON=0
ENV UV_PYTHON_DOWNLOADS=0

LABEL uk.gov.defra.python.python-version=$BASE_VERSION \
    uk.gov.defra.python.version=$DEFRA_VERSION \
    uk.gov.defra.python.repository=defradigital/python-development

RUN python -m pip install uv debugpy

USER nonroot

WORKDIR /home/nonroot

ENTRYPOINT [ "python" ]
