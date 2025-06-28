# In src/tests/test_testing_tool.py

from src.agents.testing_agent import run_pytest


def test_run_pytest_on_passing_test(tmp_path):
    """
    Tests the run_pytest tool on a test file that is expected to pass.
    """
    # Create a simple test file that will pass
    test_code = "def test_success():\n    assert 1 == 1"
    test_file = tmp_path / "test_passing.py"
    test_file.write_text(test_code)

    result = run_pytest(str(test_file))

    assert "Exit Code: 0" in result  # Exit code 0 means success
    assert "== 1 passed in" in result


def test_run_pytest_on_failing_test(tmp_path):
    """
    Tests the run_pytest tool on a test file that is expected to fail.
    """
    # Create a simple test file that will fail
    test_code = "def test_failure():\n    assert 1 == 2"
    test_file = tmp_path / "test_failing.py"
    test_file.write_text(test_code)

    result = run_pytest(str(test_file))

    assert "Exit Code: 1" in result  # Exit code 1 means failure
    assert "== 1 failed in" in result
    assert "AssertionError" in result
