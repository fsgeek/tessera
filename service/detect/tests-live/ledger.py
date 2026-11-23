"""Persistent cleanup ledger and evidence journal for Tessera V1 live detection tests.

Every throwaway resource records a durable 'creating' intent to disk BEFORE the AWS
create call so crash recovery can reconcile committed creates even if the process
dies before AWS's response is journaled.
All writes pass through safety.sanitize_value to enforce Hard Safety Rule 5
(no credentials, API keys, SQS URLs, or endpoint URLs written to output files).
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from safety import ALLOWED_REGION, SafetyViolation, sanitize_value, validate_run_id


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def save_ledger_dict(
    path: Path,
    data: dict[str, Any],
    secrets: Iterable[str] = (),
) -> None:
    """Atomically write a sanitized ledger dict to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = sanitize_value(data, secrets)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(clean, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    tmp.replace(path)


@dataclass
class RunLedger:
    run_id: str
    path: Path
    secrets: list[str] = field(default_factory=list, repr=False)
    data: dict[str, Any] = field(default_factory=dict)
    exclusive_create: bool = True
    account_id: str | None = None

    def __post_init__(self) -> None:
        validate_run_id(self.run_id)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.exclusive_create:
            # Atomic claim: O_CREAT|O_EXCL fails if any ledger for this run_id exists.
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError as exc:
                raise SafetyViolation(
                    "Ledger already exists for this run_id; refusing to overwrite or reuse run_id."
                ) from exc
            os.close(fd)
        if not self.data:
            self.data = {
                "run_id": self.run_id,
                "region": ALLOWED_REGION,
                "account_id": self.account_id,
                "started_at_utc": utc_now_iso(),
                "finished_at_utc": None,
                "resources": [],
                "events": [],
                "row_results": [],
                "alarm_transitions": [],
                "access_log_matches": [],
                "steward_mailbox_handoff": [],
                "recovery_runs": [],
                "notes": [],
            }
        self._flush()

    def _flush(self) -> None:
        save_ledger_dict(self.path, self.data, self.secrets)

    def safe_flush(self) -> bool:
        """Flush ledger without raising OSError during cleanup finally blocks."""
        try:
            self._flush()
            return True
        except OSError:
            return False

    def set_account_id(self, account_id: str) -> None:
        self.account_id = account_id
        self.data["account_id"] = account_id
        self._flush()

    def record_intent(
        self,
        resource_type: str,
        name: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Durably journal create intent BEFORE calling the AWS create API."""
        intent_id = uuid.uuid4().hex[:12]
        entry = {
            "intent_id": intent_id,
            "resource_type": resource_type,
            "identifier": None,
            "name": name,
            "intent_at_utc": utc_now_iso(),
            "created_at_utc": None,
            "status": "creating",
            "deleted_at_utc": None,
            "detail": None,
            "metadata": metadata or {},
        }
        self.data["resources"].append(entry)
        self._flush()
        return intent_id

    def confirm_created(
        self,
        intent_id: str,
        identifier: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Transition a 'creating' intent to 'active' with its non-URL identifier."""
        for entry in reversed(self.data["resources"]):
            if entry.get("intent_id") == intent_id:
                entry["identifier"] = identifier
                entry["created_at_utc"] = utc_now_iso()
                entry["status"] = "active"
                if metadata:
                    entry.setdefault("metadata", {}).update(metadata)
                self._flush()
                return
        raise RuntimeError(f"Unknown intent_id {intent_id!r} in RunLedger.confirm_created")

    def record_created(
        self,
        resource_type: str,
        identifier: str,
        name: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Record an active resource (prefer record_intent + confirm_created)."""
        intent_id = uuid.uuid4().hex[:12]
        now = utc_now_iso()
        entry = {
            "intent_id": intent_id,
            "resource_type": resource_type,
            "identifier": identifier,
            "name": name,
            "intent_at_utc": now,
            "created_at_utc": now,
            "status": "active",
            "deleted_at_utc": None,
            "detail": None,
            "metadata": metadata or {},
        }
        self.data["resources"].append(entry)
        self._flush()
        return intent_id

    def record_deleted(
        self,
        resource_type: str,
        identifier: str,
        *,
        status: str = "deleted",
        detail: str | None = None,
        intent_id: str | None = None,
        safe: bool = False,
    ) -> None:
        """Mark a tracked resource deleted, scheduled_deletion, cleanup_failed, or not_created."""
        matched = False
        for entry in reversed(self.data["resources"]):
            if intent_id is not None and entry.get("intent_id") == intent_id:
                entry["status"] = status
                if entry.get("identifier") is None and identifier:
                    entry["identifier"] = identifier
                entry["deleted_at_utc"] = utc_now_iso()
                entry["detail"] = detail
                matched = True
                break
            if (
                intent_id is None
                and entry["resource_type"] == resource_type
                and (entry.get("identifier") == identifier or entry.get("name") == identifier)
            ):
                entry["status"] = status
                entry["deleted_at_utc"] = utc_now_iso()
                entry["detail"] = detail
                matched = True
                break
        if not matched:
            self.data["resources"].append(
                {
                    "intent_id": intent_id or uuid.uuid4().hex[:12],
                    "resource_type": resource_type,
                    "identifier": identifier,
                    "name": identifier,
                    "intent_at_utc": None,
                    "created_at_utc": None,
                    "status": status,
                    "deleted_at_utc": utc_now_iso(),
                    "detail": detail,
                    "metadata": {},
                }
            )
        if safe:
            self.safe_flush()
        else:
            self._flush()

    def record_kms_scheduled_deletion(
        self,
        key_id: str,
        deletion_date_iso: str,
        *,
        intent_id: str | None = None,
        safe: bool = False,
    ) -> None:
        """Rule 6: KMS keys are reported as 'scheduled, deletes on <date>', never 'deleted'."""
        self.record_deleted(
            "kms_key",
            key_id,
            status="scheduled_deletion",
            detail=f"scheduled, deletes on {deletion_date_iso}",
            intent_id=intent_id,
            safe=safe,
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
        safe: bool = False,
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
        if safe:
            self.safe_flush()
        else:
            self._flush()

    def set_row_results(self, row_results: list[dict[str, Any]]) -> None:
        self.data["row_results"] = row_results
        self._flush()

    def set_steward_mailbox_handoff(self, handoff: list[dict[str, Any]]) -> None:
        self.data["steward_mailbox_handoff"] = handoff
        self._flush()

    def record_alarm_transition(self, transition: dict[str, Any]) -> None:
        self.data["alarm_transitions"].append(transition)
        self._flush()

    def record_access_log_matches(self, matches: list[dict[str, Any]]) -> None:
        self.data["access_log_matches"].extend(matches)
        self._flush()

    def add_note(self, note: str, *, safe: bool = False) -> None:
        self.data["notes"].append({"at_utc": utc_now_iso(), "note": note})
        if safe:
            self.safe_flush()
        else:
            self._flush()

    def finish(self) -> None:
        self.data["finished_at_utc"] = utc_now_iso()
        self.safe_flush()

    def cleanup_summary_lines(self) -> list[str]:
        lines: list[str] = []
        for r in self.data["resources"]:
            detail = f" ({r['detail']})" if r.get("detail") else ""
            raw_line = f"- [{r['status']}] {r['resource_type']} name={r['name']}{detail}"
            lines.append(sanitize_value(raw_line, self.secrets))
        return lines

    def has_uncleaned_resources(self) -> bool:
        return any(
            r["status"] not in ("deleted", "scheduled_deletion", "not_created")
            for r in self.data["resources"]
        )


def load_ledger(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
