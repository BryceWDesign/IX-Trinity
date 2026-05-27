from ix_trinity.domain import (
    ALLOWED_V0_1_RUN_MODES,
    CANONICAL_SECTOR_ORDER,
    CLOCKWISE_ORDER,
    COUNTER_CLOCKWISE_ORDER,
    AcceptanceStatus,
    RunMode,
    SafetyState,
    SectorId,
)


def test_sector_ids_are_locked_to_three_sectors() -> None:
    assert SectorId.all() == (SectorId.A, SectorId.B, SectorId.C)
    assert CANONICAL_SECTOR_ORDER == (SectorId.A, SectorId.B, SectorId.C)


def test_phase_orders_are_explicit() -> None:
    assert CLOCKWISE_ORDER == (SectorId.A, SectorId.B, SectorId.C)
    assert COUNTER_CLOCKWISE_ORDER == (SectorId.A, SectorId.C, SectorId.B)


def test_logic_only_mode_does_not_require_stored_energy() -> None:
    assert RunMode.LOGIC_ONLY.requires_stored_energy() is False
    assert RunMode.SINGLE_SECTOR.requires_stored_energy() is True


def test_baseline_modes_are_marked() -> None:
    assert RunMode.SINGLE_SECTOR.is_baseline_mode() is True
    assert RunMode.PAIRED_SECTORS.is_baseline_mode() is True
    assert RunMode.THREE_SECTOR_SIMULTANEOUS.is_baseline_mode() is True
    assert RunMode.CLOCKWISE_SEQUENCE.is_baseline_mode() is True
    assert RunMode.COUNTER_CLOCKWISE_SEQUENCE.is_baseline_mode() is True
    assert RunMode.SAFE_DUMP.is_baseline_mode() is True
    assert RunMode.FAULT_INJECTION.is_baseline_mode() is True
    assert RunMode.NO_TARGET.is_baseline_mode() is True
    assert RunMode.LOGIC_ONLY.is_baseline_mode() is False


def test_all_v0_1_run_modes_are_declared() -> None:
    assert ALLOWED_V0_1_RUN_MODES == (
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


def test_safety_state_arm_permissions_are_conservative() -> None:
    assert SafetyState.SAFE.allows_arm() is True
    assert SafetyState.READY.allows_arm() is True
    assert SafetyState.ARMED.allows_arm() is False
    assert SafetyState.BLOCKED.allows_arm() is False
    assert SafetyState.DUMP_REQUIRED.allows_arm() is False


def test_safety_state_terminal_failure_detection() -> None:
    assert SafetyState.REJECTED.is_terminal_failure() is True
    assert SafetyState.FAULTED.is_terminal_failure() is True
    assert SafetyState.BLOCKED.is_terminal_failure() is False


def test_acceptance_status_claim_permission_is_strict() -> None:
    assert AcceptanceStatus.ACCEPTED.permits_claim() is True
    assert AcceptanceStatus.REJECTED.permits_claim() is False
    assert AcceptanceStatus.INCONCLUSIVE.permits_claim() is False
    assert AcceptanceStatus.BLOCKED.permits_claim() is False
    assert AcceptanceStatus.DEMOTED.permits_claim() is False
    assert AcceptanceStatus.REQUIRES_HUMAN_REVIEW.permits_claim() is False


def test_acceptance_status_attention_flags_are_conservative() -> None:
    assert AcceptanceStatus.ACCEPTED.requires_attention() is False
    assert AcceptanceStatus.REJECTED.requires_attention() is True
    assert AcceptanceStatus.INCONCLUSIVE.requires_attention() is True
    assert AcceptanceStatus.BLOCKED.requires_attention() is True
    assert AcceptanceStatus.DEMOTED.requires_attention() is True
    assert AcceptanceStatus.REQUIRES_HUMAN_REVIEW.requires_attention() is True
