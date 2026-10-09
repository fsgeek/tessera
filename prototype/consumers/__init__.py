"""Phase-2 consumers of the throwaway Tessera prototype (THROWAWAY, not service code).

Each consumer is written from its own side: it uses only what that party would really hold,
and logs every point where it cannot do its job (BLOCKED) or cannot understand the answer
(CONFUSED), with the spec location (docs/implementation-spec.md) that leaves it there.
"""
