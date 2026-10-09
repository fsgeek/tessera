"""A tiny findings log shared by the three consumers (THROWAWAY)."""
from __future__ import annotations

from dataclasses import dataclass, field

BLOCKED = "BLOCKED"      # the consumer cannot do its job at this point
CONFUSED = "CONFUSED"    # the consumer gets an answer it cannot interpret safely
WORKED = "WORKED"        # the step worked from the consumer's side
NOTE = "NOTE"            # a fact worth recording that is neither


@dataclass
class Finding:
    consumer: str
    kind: str
    what: str
    spec: str = ""


@dataclass
class ConsumerLog:
    consumer: str
    items: list[Finding] = field(default_factory=list)

    def add(self, kind: str, what: str, spec: str = "") -> None:
        self.items.append(Finding(self.consumer, kind, what, spec))

    def of(self, kind: str) -> list[Finding]:
        return [f for f in self.items if f.kind == kind]

    def render(self) -> str:
        out = []
        for f in self.items:
            cite = f" [{f.spec}]" if f.spec else ""
            out.append(f"  {f.kind:8s} {f.what}{cite}")
        return "\n".join(out)
