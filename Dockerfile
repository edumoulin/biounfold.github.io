# Dockerfile
FROM python:3.11-slim

# System deps you actually need
RUN apt-get update && apt-get install -y --no-install-recommends \
    git tini && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Create the project venv
RUN python -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV HOME=/work

# Install pinned deps (exported by uv on the host)
COPY requirements.lock.txt /work/
RUN pip install --no-cache-dir -r /work/requirements.lock.txt

# (Optional) Keep pyproject for jupytext config, etc.
COPY pyproject.toml /work/

EXPOSE 8888
ENTRYPOINT ["tini","--"]
CMD ["jupyter","lab","--ip=0.0.0.0","--port=8888","--no-browser","--NotebookApp.token="]
