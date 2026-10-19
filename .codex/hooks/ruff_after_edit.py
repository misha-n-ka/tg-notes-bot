"""Format and lint Python files named in an apply_patch hook event."""

import json
import subprocess
import sys
from pathlib import Path


def run_hook(event: dict, root: Path) -> int:
    patch = event.get("tool_input", {}).get("command", "")
    files = set()
    for line in patch.splitlines():
        if line.startswith(("*** Add File: ", "*** Update File: ", "*** Move to: ")):
            path = (root / line.split(": ", 1)[1]).resolve()
            if path.is_relative_to(root) and path.suffix == ".py" and path.is_file():
                files.add(str(path))
    if not files:
        return 0

    ruff = root / ".venv/bin/ruff"
    if not ruff.is_file():
        print(
            "Ruff недоступен: выполните форматирование и линтер вручную.",
            file=sys.stderr,
        )
        return 2

    failed = False
    for command in ("format", "check"):
        result = subprocess.run(
            [str(ruff), command, "--", *sorted(files)],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            failed = True
            print(result.stdout + result.stderr, file=sys.stderr, end="")
    return 2 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(run_hook(json.load(sys.stdin), Path(__file__).resolve().parents[2]))
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"Хук Ruff не выполнен: {error}", file=sys.stderr)
        sys.exit(2)
