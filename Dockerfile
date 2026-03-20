# Set default values for build arguments
ARG DEFRA_VERSION=2.3.1
ARG BASE_VERSION=3.14.3-slim-trixie
ARG PYTHON_VERSION=3.14.3

# Builder stage to support backporting packages from Debian testing
# See [IMAGE_SCANNING.md](IMAGE_SCANNING.md) for details on the backporting process and considerations.
FROM python:${BASE_VERSION} AS builder

RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        dpkg-dev \
        debian-keyring \
        devscripts \
        equivs \
    && rm -rf /var/lib/apt/lists/*

RUN printf "Types: deb-src\nURIs: http://deb.debian.org/debian\nSuites: testing\nComponents: main\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg\n" > /etc/apt/sources.list.d/testing-src.sources \
    && apt update

FROM python:${BASE_VERSION} AS production

ARG DEFRA_VERSION
ARG BASE_VERSION
ARG PYTHON_VERSION

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
        ca-certificates

RUN rm -rf /var/lib/apt/lists/*

# Install Internal CA certificate for firewall and Zscaler proxy
COPY certificates/internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt

RUN chmod 644 /usr/local/share/ca-certificates/internal-ca.crt && update-ca-certificates

# Upgrade system pip (run as root so the system-wide pip is replaced)
RUN python -m pip install --upgrade --force-reinstall pip

# Create a non-root user for running Python applications
RUN addgroup --gid 1000 nonroot \
    && adduser nonroot \
        --uid 1000 \
        --gid 1000 \
        --home /home/nonroot \
        --shell /bin/bash

USER nonroot

WORKDIR /home/nonroot

ENTRYPOINT [ "python" ]

FROM production AS development

ARG DEFRA_VERSION
ARG BASE_VERSION
ARG PYTHON_VERSION

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
