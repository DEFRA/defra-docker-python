# Set default values for build arguments
ARG DEFRA_VERSION=1.1.4
ARG BASE_VERSION=3.13.9-slim-trixie

FROM python:${BASE_VERSION} AS production

ARG DEFRA_VERSION
ARG BASE_VERSION

ENV PATH="/home/nonroot/.local/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=production

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

RUN python -m pip install --no-cache-dir uv

ENTRYPOINT [ "python" ]

FROM production AS development

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=development

LABEL uk.gov.defra.python.python-version=$BASE_VERSION \
    uk.gov.defra.python.version=$DEFRA_VERSION \
    uk.gov.defra.python.repository=defradigital/python-development

RUN python -m pip install pydebug

USER nonroot
WORKDIR /home/nonroot

ENTRYPOINT [ "python" ]
