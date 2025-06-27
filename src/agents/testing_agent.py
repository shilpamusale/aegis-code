# In src/agents/testing_agent.py

import subprocess
import os
from typing import Dict, Callable

# --- ATOMIC TOOL ---


def run_pytest(target: str = ".") -> str:
    """
    Executes the pytest command on a specified target directory or file.

    This tool is the core of the TestingAgent's capabilities, allowing it
    to run automated test and validate code changes. It captures and returns
    all output, including standard output, errors, and the exit code, so the
    agent has full context on the test results.

    Args:
        target: The specific file or directory to run pytest on.
                Defaults to the current directory (".").
    Returns:
        A formatted string containing the results of the pytest execution,
        including stdout, stderr, and the retrun code.
    """

    try:
        # We use subprocess.run to execute the command.
        # 'capture_output=True' captures stedout and stderr.
        # 'text=True' ensures the output is decoded as a string.
        # 'timeout' is a safety mechanism to prevent runaway processes.

        result = subprocess.run(
            ["pytest", target],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # Structure the output clearly for the LLM to parse.
        output = "--- Pytest Execution Summary---\n"
        output += f"Exit code: {result.returncode} \n"

        if result.stdout:
            output += f"\n --- STDOUT ---\n {result.stdout}\n"

        if result.stderr:
            output += f"\n--- STDERR --- \n{result.stderr}\n"
        output += "--- End of Summary ---"
    except FileNotFoundError:
        return "Error: 'pytest' command not found. Make sure pytest is installed in the environment."
    except subprocess.TimeoutExpired:
        return "Error: Pytest execution timed out after 120 seconds."
    except Exception as e:
        return f"Error: An unexpected error occurred while running pytest: {e}"


class TestingAgent:
    """
    An agent specialized in running tests to verify code functionaity.

    This agent's primary tool is a wrapper around the pytest command-line tool.
    It is a crucial component if the Test-Driven Developmet (TDD) loop within the
    multi-agent system. After the RefactoringAgent modifies code, the TestingAgent is called
    to ensure that all tests still pass.
    """

    def __init__(self):
        """
        Initializes the agent with a dictionary of its available tools.
        """

        self.tools: Dict[str, Callable[..., str]] = {
            "run_pytest": run_pytest,
        }

    def run_dummy_test(self):
        """
        A simple local test to demonstrate the pytest tool in action.
        This test creates temporary files, runs pytest on them, and cleans up.
        """
        print("--- TestingAgent: Dummy Test Run ---")

        # 1. Create a dummy code file to test
        code_to_test = "def add(a, b):\n    return a + b\n"
        with open("temp_code.py", "w") as f:
            f.write(code_to_test)
        print("\n1. Created 'temp_code.py' for testing.")

        # 2. Create a dummy test file that should pass
        passing_test = "from temp_code import add\n\ndef test_add_success():\n    assert add(2, 3) == 5\n"
        with open("test_passing.py", "w") as f:
            f.write(passing_test)
        print("\n2. Created 'test_passing.py'.")

        # 3. Run pytest on the passing test
        print("\n3. Running pytest on the passing test...")
        result_passing = self.tools["run_pytest"]("test_passing.py")
        print(result_passing)

        # 4. Create a dummy test file that should fail
        failing_test = "from temp_code import add\n\ndef test_add_failure():\n    assert add(2, 2) == 5\n"
        with open("test_failing.py", "w") as f:
            f.write(failing_test)
        print("\n4. Created 'test_failing.py'.")

        # 5. Run pytest on the failing test
        print("\n5. Running pytest on the failing test...")
        result_failing = self.tools["run_pytest"]("test_failing.py")
        print(result_failing)

        # 6. Clean up the temporary files
        print("\n6. Cleaning up temporary files...")
        os.remove("temp_code.py")
        os.remove("test_passing.py")
        os.remove("test_failing.py")
        print("   Cleanup complete.")
        print("\n--- TestingAgent: Dummy Test Complete ---")
