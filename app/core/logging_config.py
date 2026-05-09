"""Logging setup helpers for the application."""

import logging


def setup_logging(level: str = "INFO") -> None:
    """Configure process-wide logging format and level."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
