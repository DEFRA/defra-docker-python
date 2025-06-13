# Set default values for build arguments
ARG PARENT_VERSION=latest-3.12
ARG PORT=8085
ARG PORT_DEBUG=8086

FROM defradigital/python-development:${PARENT_VERSION} AS development

ENV PATH="/home/nonroot/.venv/bin:${PATH}"
ENV LOG_CONFIG="logging-dev.json"

WORKDIR /home/nonroot

COPY --chown=nonroot:nonroot pyproject.toml .
COPY --chown=nonroot:nonroot uv.lock .

RUN uv venv \
    && uv sync --frozen --no-cache

COPY --chown=nonroot:nonroot app/ ./app/
COPY --chown=nonroot:nonroot logging-dev.json .

ARG PORT=8085
ARG PORT_DEBUG=8086
ENV PORT=${PORT}
EXPOSE ${PORT} ${PORT_DEBUG}

CMD  [ "-m", "app.main" ]

FROM defradigital/python:${PARENT_VERSION} AS production

ENV PATH="/home/nonroot/.venv/bin:${PATH}"
ENV LOG_CONFIG="logging.json"

WORKDIR /home/nonroot

COPY --chown=nonroot:nonroot --from=development /home/nonroot/.venv .venv/

COPY --chown=nonroot:nonroot --from=development /home/nonroot/app/ ./app/
COPY --chown=nonroot:nonroot logging.json .

ARG PORT
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD  [ "-m", "app.main" ]
