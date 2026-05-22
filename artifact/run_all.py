from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    run([sys.executable, "run_guarded_fsm_sim.py"])
    run([sys.executable, "artifact/validate_artifact.py"])
    run([sys.executable, "-m", "unittest", "discover", "-s", "artifact/tests", "-p", "test_*.py"])


if __name__ == "__main__":
    main()
