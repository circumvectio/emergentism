"""Compatibility package for the numbered `10_SPRINT_GATES/` tool lane."""

from pathlib import Path

_ACTUAL_PACKAGE = Path(__file__).resolve().parents[1] / "10_SPRINT_GATES"

# Let `import sprint_gates.sprint_first_cell` resolve into the numbered folder
# without renaming the on-disk lane.
__path__ = [str(_ACTUAL_PACKAGE)]
