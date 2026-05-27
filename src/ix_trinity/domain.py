"""Core domain models for IX-Trinity v0.1.

The domain layer intentionally contains small, explicit primitives that later
storage, switching, sensing, evidence, and scale-up modules can share without
creating circular dependencies.
"""

from __future__ import annotations

from enum import Enum
from typing import Final


class SectorId(str, Enum):
    """The three isolated IX-Trinity storage/discharge sectors."""

    A = "A"
    B = "B"
    C = "C"

    @classmethod
    def all(cls) -> tuple["SectorId", "SectorId", "SectorId"]:
        """Return sectors in canonical clockwise order."""
        return (cls.A, cls.B, cls.C)


class RunMode(str, Enum):
    """Supported v0.1 run modes.

    These modes are low-energy software/testbed modes. They do not authorize
    high-voltage, plasma, superconducting, fusion, or destructive operation.
    """

    LOGIC_ONLY = "logic_only"
    SINGLE_SECTOR = "single_sector"
    PAIRED_SECTORS = "paired_sectors"
    THREE_SECTOR_SIMULTANEOUS = "three_sector_simultaneous"
    CLOCKWISE_SEQUENCE = "clockwise_sequence"
    COUNTER_CLOCKWISE_SEQUENCE = "counter_clockwise_sequence"
    SAFE_DUMP = "safe_dump"
    FAULT_INJECTION = "fault_injection"
    NO_TARGET = "no_target"

    def requires_stored_energy(self) -> bool:
        """Return whether the run mode may require an armed storage sector."""
        return self is not RunMode.LOGIC_ONLY

    def is_baseline_mode(self) -> bool:
        """Return whether this mode is part of the v0.1 baseline matrix."""
        return self in {
            RunMode.SINGLE_SECTOR,
            RunMode.PAIRED_SECTORS,
            RunMode.THREE_SECTOR_SIMULTANEOUS,
            RunMode.CLOCKWISE_SEQUENCE,
            RunMode.COUNTER_CLOCKWISE_SEQUENCE,
            RunMode.SAFE_DUMP,
            RunMode.FAULT_INJECTION,
            RunMode.NO_TARGET,
        }


class SafetyState(str, Enum):
    """Safety state for a sector, run, or system-level gate."""

    SAFE = "safe"
    READY = "ready"
    ARMED = "armed"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    FAULTED = "faulted"
    DUMP_REQUIRED = "dump_required"
    DUMPED = "dumped"

    def allows_arm(self) -> bool:
        """Return whether this state allows progression toward arming."""
        return self in {SafetyState.SAFE, SafetyState.READY}

    def is_terminal_failure(self) -> bool:
        """Return whether this state represents a hard failed condition."""
        return self in {SafetyState.REJECTED, SafetyState.FAULTED}


class AcceptanceStatus(str, Enum):
    """Review outcome for evidence, runs, shots, or scale-up requests."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"
    BLOCKED = "blocked"
    DEMOTED = "demoted"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"

    def permits_claim(self) -> bool:
        """Return whether this status permits a bounded claim."""
        return self is AcceptanceStatus.ACCEPTED

    def requires_attention(self) -> bool:
        """Return whether this status requires review before any reuse."""
        return self in {
            AcceptanceStatus.REJECTED,
            AcceptanceStatus.INCONCLUSIVE,
            AcceptanceStatus.BLOCKED,
            AcceptanceStatus.DEMOTED,
            AcceptanceStatus.REQUIRES_HUMAN_REVIEW,
        }


PROJECT_NAME: Final[str] = "IX-Trinity"
V0_1_STAGE_NAME: Final[str] = "low-energy tri-sector storage/discharge testbed"

CANONICAL_SECTOR_ORDER: Final[tuple[SectorId, SectorId, SectorId]] = SectorId.all()

CLOCKWISE_ORDER: Final[tuple[SectorId, SectorId, SectorId]] = (
    SectorId.A,
    SectorId.B,
    SectorId.C,
)

COUNTER_CLOCKWISE_ORDER: Final[tuple[SectorId, SectorId, SectorId]] = (
    SectorId.A,
    SectorId.C,
    SectorId.B,
)

ALLOWED_V0_1_RUN_MODES: Final[tuple[RunMode, ...]] = (
    RunMode.LOGIC_ONLY,
    RunMode.SINGLE_SECTOR,
    RunMode.PAIRED_SECTORS,
    RunMode.THREE_SECTOR_SIMULTANEOUS,
    RunMode.CLOCKWISE_SEQUENCE,
    RunMode.COUNTER_CLOCKWISE_SEQUENCE,
    RunMode.SAFE_DUMP,
    RunMode.FAULT_INJECTION,
    RunMode.NO_TARGET,
)
