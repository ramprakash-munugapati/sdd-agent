#!/usr/bin/env python3
"""bootstrap.py – Idempotent setup for the SDD agent.

Creates a local virtual environment, installs declared dependencies: vetores: REQ-002, REQ-003`)). Not overwriting existing instructions or generating a second server.

Usage:
    python bootstrap.py

Side effects:
 * Creates .venv/ (or reuses existing) in the project root.
 * Installs pytest, coverage, jsonschema (for future tests).
 * Writes a marker file .sdd_bootstrap_done so repeated runs are no‑ops.
"""

import sys
from pathlib import Path
import subprocess
import venv

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
BOOTMARK = ROOT / ".sdd_bootstrap_done"


def main():
    # Idempotency guard
    if BOOTMARK.exists():
        print(".sdd_bootstrap_done marker present – skipping re‑initialisation.")
        return

    # Create (or reuse) virtual environment
    if not VENV_DIR.is_dir():
        print(f"Creating virtual environment at {VENV_DIR} …")
        VENV_DIR.mkdir(parents=True, exist_ok=True)
        venv.main([str(VENV_DIR), "--clear"])
    else:
        print(f"Reusing existing virtual environment at {VENV_DIR}.")

    # Determine python executable inside venv
    if sys.platform.startswith("win"):
        python_exe = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"

    # Install core test/dev packages
    packages = ["pytest", "coverage", "jsonschema", "requests"]
    print(f"Installing packages: {', '.join(packages)} …")
    subprocess.check_call([str(python_exe), "-m", "pip", "install", "--upgrade", *packages])

    # Ensure .sdd directories exist (without touching any user instructions)
    (ROOT / ".sdd").mkdir(parents=True, exist_ok=True)
    (ROOT / ".sdd" / "evidence").mkdir(parents=True, exist_ok=True)
    (ROOT / ".sdd" / "approvals.json").touch()

    # Write marker so next run is a no‑op
    BOOTMARK.touch()
    print("Bootstrap complete. Marker written at .sdd_bootstrap_done")


if __name__ == "__main__":
    main()