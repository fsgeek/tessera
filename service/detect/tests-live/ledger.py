"""Persistent cleanup ledger and evidence journal for Tessera V1 live detection tests.

Every throwaway resource is recorded to disk immediately upon creation so that
even an interrupted run leaves a complete list for crash-recovery cleanup.
All writes pass through safety.sanitize_value to enforce Hard Safety Rule 5
(no credentials, API keys, or endpoint URLs written to output files).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safety import ALLOWED_REGION, sanitize_value


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


@dataclass
class RunLedger:
    run_id: str
    path: Path
    secrets: list[str] = field(default_factory=list, repr=False)
    data: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data:
            self.data = {
                "run_id": self.run_id,
                "region": ALLOWED_REGION,
                "started_at_utc": utc_now_iso(),
                "finished_at_utc": None,
                "resources": [],
                "events": [],
                "sns_messages": [],
                "alarm_transitions": [],
                "notes": [],
            }
        self._flush()

    def _flush(self) -> None:
        clean = sanitize_value(self.data, self.secrets)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(clean, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        tmp.replace(self.path)

    def record_created(
        self,
        resource_type: str,
        identifier: str,
        name: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        entry = {
            "resource_type": resource_type,
            "identifier": identifier,
            "name": name,
            "created_at_utc": utc_now_iso(),
            "status": "active",
            "deleted_at_utc": None,
            "detail": None,
            "metadata": metadata or {},
        }
        self.data["resources"].append(entry)
        self._flush()

    def record_deleted(
        self,
        resource_type: str,
        identifier: str,
        *,
        status: str = "deleted",
        detail: str | None = None,
    ) -> None:
        """Mark a tracked resource deleted, scheduled_deletion (KMS), or cleanup_failed."""
        matched = False
        for entry in reversed(self.data["resources"]):
            if entry["resource_type"] == resource_type and entry["identifier"] == identifier:
                entry["status"] = status
                entry["deleted_at_utc"] = utc_now_iso()
                entry["detail"] = detail
                matched = True
                break
        if not matched:
            self.data["resources"].append(
                {
                    "resource_type": resource_type,
                    "identifier": identifier,
                    "name": identifier,
                    "created_at_utc": None,
                    "status": status,
                    "deleted_at_utc": utc_now_iso(),
                    "detail": detail,
                    "metadata": {},
                }
            )
        self._flush()

    def record_kms_scheduled_deletion(self, key_id: str, deletion_date_iso: str) -> None:
        """Rule 6: KMS keys are reported as 'scheduled, deletes on <date>', never 'deleted'."""
        self.record_deleted(
            "kms_key",
            key_id,
            status="scheduled_deletion",
            detail=f"scheduled, deletes on {deletion_date_iso}",
        )

    def record_event(
        self,
        row_ids: list[str],
        action: str,
        *,
        resource_name: str | None = None,
        started_at_utc: str,
        ended_at_utc: str,
        cloudtrail_event_id: str | None = None,
        request_ids: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.data["events"].append(
            {
                "row_ids": row_ids,
                "action": action,
                "resource_name": resource_name,
                "started_at_utc": started_at_utc,
                "ended_at_utc": ended_at_utc,
                "cloudtrail_event_id": cloudtrail_event_id,
                "request_ids": request_ids or [],
                "details": details or {},
            }
        )
        self._flush()

    def record_sns_message(self, message: dict[str, Any]) -> None:
        self.data["sns_messages"].append(message)
        self._flush()

    def record_alarm_transition(self, transition: dict[str, Any]) -> None:
        self.data["alarm_transitions"].append(transition)
        self._flush()

    def add_note(self, note: str) -> None:
        self.data["notes"].append({"at_utc": utc_now_iso(), "note": note})
        self._flush()

    def finish(self) -> None:
        self.data["finished_at_utc"] = utc_now_iso()
        self._flush()

    def cleanup_summary_lines(self) -> list[str]:
        lines: list[str] = []
        for r in self.data["resources"]:
            detail = f" ({r['detail']})" if r.get("detail") else ""
            lines.append(
                f"- [{r['status']}] {r['resource_type']} name={r['name']} id={r['identifier']}{detail}"
            )
        return lines

    def has_uncleaned_resources(self) -> bool:
        return any(
            r["status"] not in ("deleted", "scheduled_deletion")
            for r in self.data["resources"]
        )


def load_ledger(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
