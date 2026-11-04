"""Shared Anthropic client factory.

The developer shell may carry ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN for a
corporate proxy (used by Claude Code). Those break direct API access, so we load
.env with override=True, drop the proxy token and pin the public API base URL.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent
API_BASE_URL = "https://api.anthropic.com"


def make_client():
    import anthropic

    load_dotenv(REPO_ROOT / ".env", override=True)
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing — put it in .env")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", API_BASE_URL)
    if "netlight" in base_url:  # never route swarm traffic through the proxy
        base_url = API_BASE_URL
    return anthropic.Anthropic(base_url=base_url)
