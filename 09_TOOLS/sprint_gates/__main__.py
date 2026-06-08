"""Run the numbered sprint-gates dispatcher through the compatibility package."""

from pathlib import Path
import runpy

_ACTUAL_MAIN = Path(__file__).resolve().parents[1] / "10_SPRINT_GATES" / "__main__.py"
_namespace = runpy.run_path(str(_ACTUAL_MAIN))

raise SystemExit(_namespace["main"]())
