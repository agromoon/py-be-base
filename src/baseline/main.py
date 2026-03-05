from __future__ import annotations

import sys
from pathlib import Path

from alembic import command
from alembic.config import Config


def get_alembic_config() -> Config:
    """Return the Alembic configuration for this project."""
    project_root = Path(__file__).resolve().parents[2]
    alembic_ini = project_root / "alembic.ini"
    return Config(str(alembic_ini))


def run_migrations() -> None:
    """Run all pending database migrations up to head."""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")


def main() -> None:
    """Entry point for command-line usage."""
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        run_migrations()
    else:
        print("hey, master")
