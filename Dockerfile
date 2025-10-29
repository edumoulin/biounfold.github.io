FROM python:3.11-slim

# Minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install uv (single binary)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh -s -- 
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
RUN mkdir -p /app && chmod -R 777 /app

# Copy only lockfiles first for caching
COPY pyproject.toml uv.lock ./

# Create the venv (uv will place it at /app/.venv) and install locked deps
RUN uv sync --frozen --python 3.11

# Make the venv active for subsequent RUN/CMD
RUN mkdir /app/work
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
ENV HOME=/app/work
WORKDIR /app/work


# (Optionally) copy your project code if you run anything else
# COPY . /work/

EXPOSE 8888
# Use python -m to avoid any launcher edge-cases
CMD ["/app/.venv/bin/python","-m","jupyterlab","--ip=0.0.0.0","--port=8888","--no-browser","--NotebookApp.token="]

