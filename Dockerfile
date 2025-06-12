# Set default values for build arguments
ARG DEFRA_VERSION=0.1.0
ARG PYTHON_VERSION=3.12.11
ARG DEVELOPMENT_VERSION=3.12.11-slim-bookworm
ARG PRODUCTION_VERSION=cc-debian12

FROM python:${DEVELOPMENT_VERSION} AS development

ARG DEFRA_VERSION
ARG PYTHON_VERSION
ARG BASE_VERSION

ENV PATH="/home/nonroot/.local/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=development

LABEL uk.gov.defra.python.python-version=$PYTHON_VERSION \
      uk.gov.defra.python.version=$DEFRA_VERSION \
      uk.gov.defra.python.repository=defradigital/python-development

RUN apt update \
  && apt upgrade -y --no-install-recommends \
  && apt install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install curl from Debian 13 (trixie) backport to patch CVE-2025-0725
RUN echo "deb https://deb.debian.org/debian bookworm-backports main" > /etc/apt/sources.list.d/bookworm-backports.list \
  && apt update \
  && apt install -t bookworm-backports -y --no-install-recommends \
    curl \
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
    
USER nonroot
WORKDIR /home/nonroot

# Install Python package manager and development tools
RUN python -m pip install --no-cache-dir uv pydebug

ENTRYPOINT [ "/usr/local/bin/python" ]

FROM gcr.io/distroless/${PRODUCTION_VERSION}:nonroot AS production

ARG DEFRA_VERSION
ARG PYTHON_VERSION
ARG BASE_VERSION

ENV PATH="/home/nonroot/.local/bin:$PATH"
ENV LD_LIBRARY_PATH="/lib/x86_64-linux-gnu:/usr/local/lib:/usr/local/lib/python3.12/site-packages"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=production

LABEL uk.gov.defra.python.python-version=$PYTHON_VERSION \
      uk.gov.defra.python.version=$DEFRA_VERSION \
      uk.gov.defra.python.repository=defradigital/python

# Copy required debian packages from the development stage
COPY --from=development /bin/curl /bin/curl

# Copy updated CA certificates from the development stage
COPY --from=development /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=development /etc/ssl/certs /etc/ssl/certs

# Copy Python binaries and dependencies from the development stage
COPY --from=development /lib/x86_64-linux-gnu/lib* /lib/x86_64-linux-gnu/
COPY --from=development /usr/local /usr/local

# Copy Python package manager and development tools from the development stage
COPY --from=development /home/nonroot/.local/bin/uv /home/nonroot/.local/bin/uv

USER nonroot
WORKDIR /home/nonroot

ENTRYPOINT [ "/usr/local/bin/python" ]
