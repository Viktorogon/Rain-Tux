"""Global application configuration loaded from TOML (XDG config path)."""

from __future__ import annotations

import os
from pathlib import Path

import tomllib
from pydantic import BaseModel, Field


def _xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def _xdg_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def _xdg_cache_home() -> Path:
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".local" / "cache"))


DEFAULT_CONFIG_PATH = _xdg_config_home() / "raintux" / "config.toml"


class ApiConfig(BaseModel):
    """Local HTTP API binding."""

    host: str = "127.0.0.1"
    port: int = 7272


class EngineConfig(BaseModel):
    """Core engine options."""

    default_update_ms: int = Field(default=1000, ge=50)
    skins_roots: list[str] = Field(default_factory=list)


class RainTuxConfig(BaseModel):
    """Top-level config file schema."""

    api: ApiConfig = Field(default_factory=ApiConfig)
    engine: EngineConfig = Field(default_factory=EngineConfig)


def default_skins_roots() -> list[Path]:
    """Default search paths for skins (XDG + legacy ~/RainTux)."""
    home = Path.home()
    roots = [
        home / "RainTux" / "Skins",
        _xdg_data_home() / "raintux" / "skins",
        Path("/usr/share/raintux/skins") if Path("/usr/share/raintux/skins").exists() else None,
    ]
    return [p for p in roots if p is not None]


def ensure_layout() -> None:
    """Create config dir, data dir, and default skins folder if missing."""
    DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = _xdg_data_home() / "raintux"
    (data / "logs").mkdir(parents=True, exist_ok=True)
    (data / "cache").mkdir(parents=True, exist_ok=True)
    (Path.home() / "RainTux" / "Skins").mkdir(parents=True, exist_ok=True)


def load_config(path: Path | None = None) -> RainTuxConfig:
    """Load TOML config; write defaults when file does not exist."""
    ensure_layout()
    cfg_path = path or DEFAULT_CONFIG_PATH
    if not cfg_path.is_file():
        default = RainTuxConfig()
        roots = [str(p) for p in default_skins_roots()]
        default.engine.skins_roots = roots
        save_config(default, cfg_path)
        return default
    raw = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    return RainTuxConfig.model_validate(raw)


def save_config(config: RainTuxConfig, path: Path | None = None) -> None:
    """Persist config as TOML (minimal hand serialization for no extra deps)."""
    cfg_path = path or DEFAULT_CONFIG_PATH
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "[api]",
        f'host = "{config.api.host}"',
        f"port = {config.api.port}",
        "",
        "[engine]",
        f"default_update_ms = {config.engine.default_update_ms}",
        "skins_roots = [",
    ]
    for root in config.engine.skins_roots:
        lines.append(f'  "{root}",')
    lines.append("]")
    cfg_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
