from ix_trinity import __version__, project_name, project_summary


def test_project_name_is_locked() -> None:
    assert project_name() == "IX-Trinity"


def test_version_is_initial_v0_1() -> None:
    assert __version__ == "0.1.0"


def test_summary_preserves_v0_1_boundaries() -> None:
    summary = project_summary()

    assert "low-energy" in summary
    assert "evidence-gated" in summary
    assert "tri-sector" in summary
