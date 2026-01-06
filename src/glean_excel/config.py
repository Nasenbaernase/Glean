from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class GleanConfig:
    """Configuration required to send content to Glean."""

    base_url: str
    api_key: str
    app_id: str
    timeout: int = 30

    @classmethod
    def from_env(cls, *, base_url: Optional[str] = None, api_key: Optional[str] = None, app_id: Optional[str] = None, timeout: Optional[int] = None) -> "GleanConfig":
        """Create a config instance reading defaults from environment variables.

        Environment variable fallbacks:
        - ``GLEAN_BASE_URL`` (defaults to ``https://api.glean.com``)
        - ``GLEAN_API_KEY`` (required)
        - ``GLEAN_APP_ID`` (required)
        - ``GLEAN_TIMEOUT`` (seconds, defaults to 30)
        """

        resolved_base_url = base_url or os.getenv("GLEAN_BASE_URL", "https://api.glean.com")
        resolved_api_key = api_key or os.getenv("GLEAN_API_KEY")
        resolved_app_id = app_id or os.getenv("GLEAN_APP_ID")

        env_timeout = os.getenv("GLEAN_TIMEOUT")
        resolved_timeout = timeout if timeout is not None else int(env_timeout) if env_timeout else 30

        missing = [name for name, value in {"api_key": resolved_api_key, "app_id": resolved_app_id}.items() if not value]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Missing configuration values: {joined}. Provide them via arguments or environment variables.")

        return cls(
            base_url=resolved_base_url.rstrip("/"),
            api_key=resolved_api_key,  # type: ignore[arg-type]
            app_id=resolved_app_id,  # type: ignore[arg-type]
            timeout=resolved_timeout,
        )


__all__ = ["GleanConfig"]
