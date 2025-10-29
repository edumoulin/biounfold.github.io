# =========================
# BioUnfold — Make commands
# =========================
# Conventions:
# - CPU is default. Use `PROFILE=gpu` to run the GPU service (requires NVIDIA toolkit).
# - Nothing required on host beyond Docker/Compose.
# - Locking deps works with local `uv` if present; otherwise falls back to a one-off Docker run.

SHELL := /bin/bash
PROFILE ?= cpu
COMPOSE := docker compose

# Detect host UID/GID for correct file ownership; fall back to 1000
UID ?= $(shell id -u 2>/dev/null || echo 1000)
GID ?= $(shell id -g 2>/dev/null || echo 1000)
export UID GID

# -------------------------
# Existing site commands
# -------------------------
serve:
	cd docs && bundle exec jekyll serve --drafts --future --livereload

publish: publish_posts export_nbs

publish_posts:
	bash publish_posts.sh

export_nbs:
	bash export_notebooks.sh

# -------------------------
# Environment / Dependencies
# -------------------------
# Resolve and lock exact Python deps to uv.lock (from pyproject.toml).
lock:
	uv lock --python 3.11
	@echo "[lock311] Updated uv.lock for Python 3.11"

## Create/refresh local virtualenv from uv.lock (installs deps).
sync: lock
	uv sync --python 3.11
	@echo "[sync311] Installed dependencies into .venv using uv.lock"

## Convenience: default deps target does a full sync.
deps: sync

# -------------------------
# Docker lifecycle
# -------------------------
## Build the Jupyter image (CPU by default). Rebuild when pyproject.toml or uv.lock changes.
build: deps
	$(COMPOSE) --profile $(PROFILE) build

## Run Jupyter Lab, mounting the repo at /work (Ctrl+C to stop).
up:
	$(COMPOSE) --profile $(PROFILE) up

## Stop containers (keeps volumes).
down:
	$(COMPOSE) down

## Stop and remove containers + named volumes (useful to reset state).
clean:
	$(COMPOSE) down -v

## Hard cleanup of dangling images (safe to run occasionally).
nuke: clean
	docker image prune -f

# -------------------------
# Start both services
# -------------------------
# Jupyter in Docker (detached) + Jekyll in foreground
dev: up-detach serve

# Start Jupyter only, detached
up-detach:
	docker compose --profile $(PROFILE) up -d
	@echo "[dev] JupyterLab is running at http://localhost:8888"

# Best-effort stop of both
dev-stop:
	- docker compose down
	- pkill -f "bundle exec jekyll serve" || true
	@echo "[dev] Stopped Jupyter and attempted to stop Jekyll. If Jekyll persists, Ctrl-C the terminal running it."

# -------------------------
# Convenience
# -------------------------

## Open a shell in the running container (for quick checks).
sh:
	$(COMPOSE) exec lab /bin/bash || true

.PHONY: serve publish publish_posts export_nbs lock build up down clean nuke sh dev dev-stop
