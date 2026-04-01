.PHONY: install run dev ui-dev test clean

PYTHON ?= python3

# Prefer uv when available; fall back to pip editable install.
install:
	@command -v uv >/dev/null 2>&1 && uv sync || $(PYTHON) -m pip install -e ".[dev]"

run: install
	uv run raintux 2>/dev/null || $(PYTHON) -m raintux

dev: install
	RAINTUX_DEV=1 uv run raintux 2>/dev/null || RAINTUX_DEV=1 $(PYTHON) -m raintux

# Skin Manager: run RainTux first so :7272 is up; Vite defaults to port 8080 (see ui/vite.config.ts).
ui-dev:
	cd ui && npm install && npm run dev

test:
	uv run pytest 2>/dev/null || $(PYTHON) -m pytest

clean:
	rm -rf build dist *.egg-info .venv __pycache__ **/__pycache__
