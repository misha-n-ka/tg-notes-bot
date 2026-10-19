import runpy
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def hook():
    return runpy.run_path(
        str(Path(__file__).resolve().parents[1] / ".codex/hooks/ruff_after_edit.py")
    )["run_hook"]


def test_formats_then_lints_only_python_files_in_patch(hook, tmp_path):
    tmp_path = tmp_path / "repo"
    tmp_path.mkdir()
    (tmp_path / ".venv/bin").mkdir(parents=True)
    (tmp_path / ".venv/bin/ruff").touch()
    for name in ("edited.py", "untouched.py", "README.md"):
        (tmp_path / name).touch()
    outside = tmp_path.parent / "outside.py"
    outside.touch()
    event = {
        "tool_input": {
            "command": "\n".join(
                [
                    "*** Update File: edited.py",
                    "*** Add File: README.md",
                    "*** Update File: ../outside.py",
                    "*** Delete File: deleted.py",
                ]
            )
        }
    }
    with patch("subprocess.run") as run:
        run.return_value.returncode = 0
        assert hook(event, tmp_path) == 0
    assert [call.args[0] for call in run.call_args_list] == [
        [str(tmp_path / ".venv/bin/ruff"), command, "--", str(tmp_path / "edited.py")]
        for command in ("format", "check")
    ]


def test_non_python_patch_does_not_run_ruff(hook, tmp_path):
    with patch("subprocess.run") as run:
        assert (
            hook({"tool_input": {"command": "*** Update File: README.md"}}, tmp_path)
            == 0
        )
    run.assert_not_called()


def test_missing_ruff_reports_failure(hook, tmp_path):
    (tmp_path / "edited.py").touch()
    assert hook({"tool_input": {"command": "*** Add File: edited.py"}}, tmp_path) == 2


def test_lint_failure_is_reported_to_agent(hook, tmp_path, capsys):
    (tmp_path / ".venv/bin").mkdir(parents=True)
    (tmp_path / ".venv/bin/ruff").touch()
    (tmp_path / "edited.py").touch()
    with patch("subprocess.run") as run:
        run.return_value.returncode = 1
        run.return_value.stdout = "lint failed\n"
        run.return_value.stderr = ""
        assert (
            hook({"tool_input": {"command": "*** Move to: edited.py"}}, tmp_path) == 2
        )
    assert "lint failed" in capsys.readouterr().err
