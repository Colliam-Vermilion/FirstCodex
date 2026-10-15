#!/usr/bin/env python3
"""Add authorized contact settings outside the checkout, without exposing values."""
from __future__ import annotations
import json
import os
from pathlib import Path
import tempfile

runtime = Path(os.environ.get("NATURE_RUNTIME_DIR", Path(__file__).resolve().parent))
config_dir = runtime / "config"
contact_file = config_dir / "contact.json"
existing = json.loads(contact_file.read_text()) if contact_file.exists() else {}
email = os.environ.get("NATURE_CONTACT_EMAIL") or os.environ.get("PUBMED_EMAIL") or existing.get("contact_email", "")
if not email or "@" not in email:
    raise SystemExit("Set the authorized NATURE_CONTACT_EMAIL or PUBMED_EMAIL outside the repository")

def save_private(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temp = tempfile.mkstemp(prefix=".nature-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2)
            f.write("\n")
        os.chmod(temp, 0o600)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)

existing["contact_email"] = email
save_private(contact_file, existing)
lit_dl = Path(os.environ.get("LIT_DL_CONFIG_DIR", config_dir / "lit-dl"))
settings_file = lit_dl / "settings.json"
settings = json.loads(settings_file.read_text()) if settings_file.exists() else {}
settings.setdefault("open_access", {}).setdefault("contact_email", email)
save_private(settings_file, settings)
print(json.dumps({"contact_configured": True, "downloader_contact_configured": bool(settings["open_access"]["contact_email"]), "existing_settings_preserved": True}))
