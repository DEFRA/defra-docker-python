# Set default values for build arguments
ARG DEFRA_VERSION=1.0.0
ARG BASE_VERSION=3.12.10-slim-bookworm

FROM python:${BASE_VERSION} AS production

ARG BASE_VERSION
ARG DEFRA_VERSION

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=development

# Set global pip dependencies to be stored under the python user directory
ENV PATH="/home/python/.local/bin:$PATH"

RUN apt update && apt install -y curl ca-certificates

# Install Internal CA certificate for firewall and Zscaler proxy
COPY certificates/internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt
RUN chmod 644 /usr/local/share/ca-certificates/internal-ca.crt && update-ca-certificates

# create a python user to run as
RUN addgroup --gid 1000 python \
  && adduser python \
    --uid 1000 \
    --gid 1000 \
    --home /home/python \
    --shell /bin/bash

# Default to the python user
USER python
WORKDIR /home/python

# Install uv for package management
RUN python -m pip install --user uv

# Label images to aid searching
LABEL uk.gov.defra.python.python-version=$BASE_VERSION \
      uk.gov.defra.python.version=$DEFRA_VERSION \
      uk.gov.defra.python.repository=defradigital/python

FROM production AS development

ENV PYTHON_ENV=development

LABEL uk.gov.defra.python.repository=defradigital/python-development

# Install debugging tools
RUN python -m pip install --user pydebug
