# # In src/agents/refactoring_agent.py

import os
from typing import Dict, Callable

# --- ATOMIC TOOLS ---


def read_file(file_path: str) -> str:
    """
    Reads the complete content of a specified file and returns it as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        # Corrected the error message to match the test's expectation exactly.
        return "Error: File not found"
    except Exception as e:
        return f"Error: An unexpected error occurred while reading the file: {e}"


def write_file(file_path: str, content: str) -> str:
    """
    Writes new content to a specified file, overwriting any existing content.
    """
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        # Corrected the typo "wroe" to "wrote" to match the test's expectation.
        return f"Successfully wrote {len(content)} characters to '{file_path}'."
    except Exception as e:
        return f"Error: An unexpected error occurred while writing to the file: {e}"


class RefactoringAgent:
    """
    An agent specialized in modifying code by reading and writing files.
    """

    def __init__(self):
        """Initializes the agent with a dictionary of its available tools."""
        self.tools: Dict[str, Callable[..., str]] = {
            "read_file": read_file,
            "write_file": write_file,
        }

    def run_dummy_test(self):
        """
        A simple local test to demonstrate the agent's tools in action.
        """
        # (Dummy test implementation is omitted for brevity as it's not needed for the fix)
        pass
