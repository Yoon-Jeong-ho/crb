from __future__ import annotations

import subprocess
from pathlib import Path



def get_git_commit(cwd: str | Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            cwd=str(cwd),
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"
