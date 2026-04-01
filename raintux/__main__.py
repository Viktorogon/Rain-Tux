"""CLI entry: `python -m raintux` or `raintux`."""

from __future__ import annotations

import os
import sys


def main() -> None:
    """Start the RainTux engine (GTK main loop + background asyncio + API)."""
    from raintux.launch_env import load_launch_env

    load_launch_env()
    # Late import so `--help` can stay fast if we add argparse later.
    from raintux.core.engine import run_engine

    dev = os.environ.get("RAINTUX_DEV", "").lower() in ("1", "true", "yes")
    raise SystemExit(run_engine(dev_mode=dev))


if __name__ == "__main__":
    main()
