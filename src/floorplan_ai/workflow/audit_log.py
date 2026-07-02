"""Audit log helpers for synthetic officer workflow simulations."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLog:
    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []

    def record(self, action: str, actor: str = "system", details: dict[str, Any] | None = None) -> None:
        self.entries.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "actor": actor,
                "action": action,
                "details": details or {},
                "advisory_only": True,
                "synthetic_data_only": True,
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "advisory_only": True,
            "synthetic_data_only": True,
            "human_review_required": True,
            "entries": self.entries,
        }

    def write_json(self, output_path: str | Path) -> Path:
        import json

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return output
