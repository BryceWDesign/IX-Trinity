"""IX-Trinity package.

IX-Trinity is a source-available technical evaluation prototype for a bounded,
measurement-first, tri-sector pulsed-energy architecture.

The package intentionally starts with low-energy software models and evidence
gates. It does not claim production readiness, high-voltage operation,
superconducting hardware proof, plasma confinement, fusion performance, or
industrial deployment readiness.
"""

from __future__ import annotations

from ix_trinity.domain import AcceptanceStatus, RunMode, SafetyState, SectorId

__all__ = [
    "__version__",
    "AcceptanceStatus",
    "RunMode",
    "SafetyState",
    "SectorId",
    "project_name",
    "project_summary",
]

__version__ = "0.1.0"


def project_name() -> str:
    """Return the public project name."""
    return "IX-Trinity"


def project_summary() -> str:
    """Return the bounded v0.1 project summary."""
    return (
        "IX-Trinity v0.1 models a low-energy, evidence-gated, tri-sector "
        "storage/discharge architecture with explicit claim boundaries."
    )
