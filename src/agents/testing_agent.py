# In src/agents/testing_agent.py

import subprocess
from typing import Dict, Callable

# --- ATOMIC TOOL ---


def run_pytest(target: str = ".") -> str:
    """
    Executes the pytest command on a specified target directory or file.
    This version is redesigned to be more robust and always return a string.
    """
    command = ["pytest", target]
    try:
        # Execute the command and capture the output.
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # Wait for the command to complete and get the output.
        stdout, stderr = process.communicate(timeout=120)
        return_code = process.returncode

        # Format the output consistently.
        output = "--- Pytest Execution Summary ---\n"
        output += f"Exit Code: {return_code}\n"

        if stdout:
            output += f"\n--- STDOUT ---\n{stdout}\n"

        if stderr:
            output += f"\n--- STDERR ---\n{stderr}\n"

        output += "--- End of Summary ---"

        return output

    except FileNotFoundError:
        return f"Error: Command '{command[0]}' not found. Is pytest installed and in the system's PATH?"
    except subprocess.TimeoutExpired:
        process.kill()
        return "Error: Pytest execution timed out after 120 seconds."
    except Exception as e:
        # This is the ultimate fallback to ensure a string is always returned.
        return f"Error: An unexpected error occurred while running pytest: {str(e)}"


class TestingAgent:
    """
    An agent specialized in running tests to verify code functionality.
    """

    def __init__(self):
        """Initializes the agent with a dictionary of its available tools."""
        self.tools: Dict[str, Callable[..., str]] = {
            "run_pytest": run_pytest,
        }


# (The local test block is omitted for clarity)
