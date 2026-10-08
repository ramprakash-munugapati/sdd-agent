"""Deterministic tests for the SDD agent – REQ-016 coverage.

These tests exercise the validation, approval, and CLI agreement logic
without requiring a real Gradle project.
"""

import hashlib
import json
import os
import subprocess
import sys
import time
import tempfile
from pathlib import Path

# --------------------------------------------------------------------- #
# Test configuration
# --------------------------------------------------------------------- #
# Repository root – the sdd-agent directory (parent of the tests folder)
REPO_ROOT = Path(__file__).parent

# Absolute path to the CLI script – used by subprocess calls so that
# the module name 'sdd_agent' is not relied upon (which can fail when
# the cwd of the subprocess is not the repository root).
SCRIPT = REPO_ROOT / "sdd_agent.py"
    sha256_file,
    validate_spec,
    validate_plan,
    validate_tasks,
    record_approval,
    check_approval_valid,
    load_approvals,
    save_approvals,
    APPROVALS_FILE,
)
import sdd_agent

REPO_ROOT = Path(__file__).parent
SCRIPT = REPO_ROOT / "sdd_agent.py"


# --------------------------------------------------------------------- #
# Helper functions (mirrored from sdd_agent for test isolation)
# --------------------------------------------------------------------- #

def write_file(path: Path, content: str):
    path.write_text(content)


# --------------------------------------------------------------------- #
# Artifact validation tests
# --------------------------------------------------------------------- #


def test_validate_spec_missing():
    """REQ-002 – SPEC.md must contain REQ-XXX."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            ok, msg = validate_spec()
            assert not ok, "Expected validate_spec to fail on missing SPEC.md"
            assert "missing" in msg.lower()
        finally:
            sdd_agent.PROJECT_DIR = old


def test_validate_spec_ok():
    """REQ-002 – valid SPEC.md passes."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            write_file(sdd_agent.PROJECT_DIR / "SPEC.md", "REQ-001: do something\n")
            ok, msg = validate_spec()
            assert ok, f"Expected validate_spec to pass, got: {msg}"
        finally:
            sdd_agent.PROJECT_DIR = old


def test_validate_plan_required_sections():
    """REQ-003 – PLAN.md must have the four required sections."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            write_file(
                sdd_agent.PROJECT_DIR / "PLAN.md",
                "architecture: modular\n"
                "execution steps: build, test\n"
                "requirement mapping: REQ-001 -> TASK-001\n"
                "validation strategy: checkstyle, jacoco\n",
            )
            ok, msg = validate_plan()
            assert ok, f"Expected validate_plan to pass, got: {msg}"
        finally:
            sdd_agent.PROJECT_DIR = old


def test_validate_plan_missing():
    """REQ-003 – missing required sections fails."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            write_file(sdd_agent.PROJECT_DIR / "PLAN.md", "some random text")
            ok, msg = validate_plan()
            assert not ok, "Expected validate_plan to fail on missing sections"
            # at least one of the required phrases should be absent
            missing_phrases = ["architecture", "execution steps", "requirement mapping", "validation strategy"]
            assert any(p in msg.lower() for p in missing_phrases), f"Message did not mention missing sections: {msg}"
        finally:
            sdd_agent.PROJECT_DIR = old


def test_validate_tasks_unique_ids():
    """REQ-004 – TASKS.json must have unique IDs."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            write_file(
                sdd_agent.PROJECT_DIR / "TASKS.json",
                json.dumps({"tasks": [
                    {"id": "TASK-001", "title": "First", "requirements": ["REQ-001"]},
                    {"id": "TASK-001", "title": "Duplicate", "requirements": ["REQ-002"]},
                ]}),
            )
            ok, msg = validate_tasks()
            assert not ok, "Expected validate_tasks to reject duplicate IDs"
            assert "duplicate" in msg.lower()
        finally:
            sdd_agent.PROJECT_DIR = old


def test_validate_tasks_missing_fields():
    """REQ-004 – tasks must have id, title, requirements."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            write_file(
                sdd_agent.PROJECT_DIR / "TASKS.json",
                json.dumps({"tasks": [{"title": "Missing ID", "requirements": ["REQ-001"]}]})
            )
            ok, msg = validate_tasks()
            assert not ok, "Expected validate_tasks to reject missing id"
            assert "missing" in msg.lower() or "id" in msg.lower()
        finally:
            sdd_agent.PROJECT_DIR = old


# --------------------------------------------------------------------- #
# Approval fingerprint tests
# --------------------------------------------------------------------- #


def test_approval_record_and_check():
    """REQ-005 / REQ-006 – record approval and fingerprint check."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            # Write a SPEC.md so sha256 is deterministic
            spec_content = "REQ-001: implement feature\n"
            write_file(sdd_agent.PROJECT_DIR / "SPEC.md", spec_content)
            # Record approval
            record_approval("spec", "Owner")
            approvals = load_approvals()
            assert "spec" in approvals, "Approval should be recorded"
            # Fingerprint should match
            fingerprint = sha256_file(sdd_agent.PROJECT_DIR / "SPEC.md")
            assert approvals["spec"]["fingerprint"] == fingerprint
            # Check validity
            valid = check_approval_valid("spec")
            assert valid, "check_approval_valid should return True for unchanged spec"
            # Now modify spec and check invalidation
            write_file(sdd_agent.PROJECT_DIR / "SPEC.md", "REQ-001: new feature\n")
            valid_after_change = check_approval_valid("spec")
            assert not valid_after_change, "Approval should be invalid after spec change"
            print("approval record/check tests passed")
        finally:
            sdd_agent.PROJECT_DIR = old


def test_approval_invalidation_on_plan_change():
    """REQ-006 – plan approval invalidated when plan changes but spec unchanged."""
    with tempfile.TemporaryDirectory() as tmp:
        old = sdd_agent.PROJECT_DIR
        sdd_agent.PROJECT_DIR = Path(tmp)
        try:
            spec_text = "REQ-001: implement\n"
            plan_text = "architecture: monolith\nexecution steps: build\ntask mapping: REQ-001 -> TASK-001\nvalidation strategy: checkstyle\n"
            write_file(sdd_agent.PROJECT_DIR / "SPEC.md", spec_text)
            write_file(sdd_agent.PROJECT_DIR / "PLAN.md", plan_text)
            record_approval("plan", "Owner")
            approvals = load_approvals()
            assert check_approval_valid("plan")
            # Change plan only
            plan_text2 = "architecture: microkern\nexecution steps: build\ntask mapping: REQ-001 -> TASK-001\nvalidation strategy: checkstyle\n"
            write_file(sdd_agent.PROJECT_DIR / "PLAN.md", plan_text2)
            valid_after_plan_change = check_approval_valid("plan")
            assert not valid_after_plan_change, "Plan approval should be invalidated when plan changes"
            print("plan change invalidation test passed")
        finally:
            sdd_agent.PROJECT_DIR = old


# --------------------------------------------------------------------- #
# CLI command tests – using the script directly
# --------------------------------------------------------------------- #


def run_script(args):
    """Run sdd_agent.py with given args, capture returncode, stdout, stderr."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result


def test_cli_check_command_exit_code():
    """REQ-013 – `check` returns zero on success, non-zero on failure."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        tmp_dir.mkdir(parents=True, exist_ok=True)
        (tmp_dir / "SPEC.md").write_text("REQ-001: do work\n")
        result = run_script(["check", "--project", str(tmp_dir)])
        assert result.returncode == 0, f"check should exit 0, got {result.returncode}: {result.stdout} {result.stderr}"
    print("CLI check exit-code test passed")


def test_cli_approve_command():
    """REQ-013 – `approve` records approval and exits 0."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        tmp_dir.mkdir(parents=True, exist_ok=True)
        (tmp_dir / "SPEC.md").write_text("REQ-001: do work\n")
        result = run_script(["approve", "spec", "--reviewer", "TestOwner", "--project", str(tmp_dir)])
        assert result.returncode == 0, f"approve should exit 0, got {result.returncode}: {result.stdout} {result.stderr}"
        # Verify fingerprint stored
        approvals_file = tmp_dir / ".sdd" / "approvals.json"
        assert approvals_file.exists(), "approvals.json should be created"
        data = json.loads(approvals_file.read_text())
        assert data["spec"]["reviewer"] == "TestOwner"
    print("CLI approve test passed")


def test_serve_endpoints():
    """REQ-013 – serve command starts HTTP server and responds on loopback."""
    import urllib.request

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        tmp_dir.mkdir(parents=True, exist_ok=True)
        (tmp_dir / "SPEC.md").write_text("REQ-001: do work\n")
        # start serve in background using the script directly
        proc = subprocess.Popen(
            [sys.executable, str(SCRIPT), "serve", "--project", str(tmp_dir), "--port", "12345"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=REPO_ROOT,
        )
        # wait for server to start, polling port
        deadline = time.time() + 10
        server_up = False
        while time.time() < deadline:
            try:
                resp = urllib.request.urlopen("http://127.0.0.1:12345/", timeout=1)
                server_up = True
                break
            except Exception:
                time.sleep(0.3)
        if not server_up:
            proc.terminate()
            proc.wait()
            raise AssertionError("Serve did not start within 10 seconds")
        try:
            # GET /
            resp = urllib.request.urlopen("http://127.0.0.1:12345/")
            assert resp.status == 200, f"Expected 200, got {resp.status}"
            # GET /api/sdd/status
            resp2 = urllib.request.urlopen("http://127.0.0.1:12345/api/sdd/status")
            status = json.loads(resp2.read())
            assert "project" in status, f"Status missing project key: {status}"
            # POST /api/sdd/verify
            req = urllib.request.Request(
                "http://127.0.0.1:12345/api/sdd/verify",
                data=b"{}",
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            resp3 = urllib.request.urlopen(req)
            verify_result = json.loads(resp3.read())
            assert "valid" in verify_result, f"Verify result missing valid key: {verify_result}"
        finally:
            proc.terminate()
            proc.wait()
    print("Serve endpoint test passed")


# --------------------------------------------------------------------- #
# Main test runner
# --------------------------------------------------------------------- #

if __name__ == "__main__":
    # Run all tests and report
    tests = [
        ("test_validate_spec_missing", test_validate_spec_missing),
        ("test_validate_spec_ok", test_validate_spec_ok),
        ("test_validate_plan_required_sections", test_validate_plan_required_sections),
        ("test_validate_plan_missing", test_validate_plan_missing),
        ("test_validate_tasks_unique_ids", test_validate_tasks_unique_ids),
        ("test_validate_tasks_missing_fields", test_validate_tasks_missing_fields),
        ("test_approval_record_and_check", test_approval_record_and_check),
        ("test_approval_invalidation_on_plan_change", test_approval_invalidation_on_plan_change),
        ("test_cli_check_command_exit_code", test_cli_check_command_exit_code),
        ("test_cli_approve_command", test_cli_approve_command),
        ("test_serve_endpoints", test_serve_endpoints),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS: {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL: {name} – {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")
    sys.exit(0 if failed == 0 else 1)