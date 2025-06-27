# In src/agents/refactoring_agent.py

import os
from typing import Dict, Callable

# -- ATOMIC TOOLS ---
# These are the fundamental building blocks for the agent's capabilities.
# Each tool does one thing and does it well.


def read_file(file_path: str) -> str:
    """
    Reads the complete content of a specified file and returns it as a string.

    This tool is essential for the agent to get the context of the code
    it needs to refactor. It is a "read-only" operation.

    Args:
        file_path: The relative or absolute path to the file to be read.
    Returns:
        A string containing the file's content, or an error message if the file cannot be read.

    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"ERROR: file not found at '{file_path}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred while reading the file: {e}"


def write_fie(file_path: str, content: str) -> str:
    """
    Writes new content to a specified file, overwritng any existing content.

    This is the primary "write" tool for the agent, allowing it to save its refactored code.

    Args:
        file_path: The relative or absolute path to the file to be written.
        content: The new string content to write to the file.

    Returns:
        A success or error message as a string.
    """
    try:
        # Ensure the directory exists before writing the file.
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wroe {len(content)} characters to '{file_path}'"
    except Exception as e:
        return f"Error: An unexpected error occurred while writing to the file: {e}"


class RefactoringAgent:
    """
    As agent specialized in modifying code by reading and writing files.

    This agent is equipped with fundamental file system tools. It forms the core of the "execution"
    capability for the code modernaizaton workflow. The agent's logic uses LangGrapg to decide when to
    read a file, pass its content to an LLM for refactoring, and then use the write tool to save the result.

    """

    def __init__(self):
        """
        Initializes the agent with a dictionary of ots available tools.
        """
        self.tools: Dict[str, Callable[..., str]] = {
            "read_file": read_file,
            "write_file": write_fie,
        }

    def run_dummy_test(self):
        """
        A simple local test to demonstrate the agent's tools in action.
        This does not involve an LLM.
        """

        print("--- RefactoringAgent: Dummy Test Run ---")
        test_file_path = "temp_test_file.py"
        original_code = "def hello_world():\n    print('Hello, old world!')"
        refactored_code = 'def hello_world():\n    """Greets the new world."""\n    print(\'Hello, brave new world!\')'

        # 1. Write the original code
        print(f"\n1. Writing original code to '{test_file_path}'...")
        status = self.tools["write_file"](test_file_path, original_code)
        print(f"   Status: {status}")

        # 2. Read the original code
        print(f"\n2. Reading original code from '{test_file_path}'...")
        read_content = self.tools["read_file"](test_file_path)
        print("   Content:\n---\n" + read_content + "\n---")

        # 3. Write the refactored code
        print(f"\n3. Writing refactored code to '{test_file_path}'...")
        status = self.tools["write_file"](test_file_path, refactored_code)
        print(f"   Status: {status}")

        # 4. Verify the new content
        print(f"\n4. Verifying new content in '{test_file_path}'...")
        final_content = self.tools["read_file"](test_file_path)
        print("   Final Content:\n---\n" + final_content + "\n---")

        # 5. Clean up the test file
        print("\n5. Cleaning up...")
        os.remove(test_file_path)
        print(f"   Removed '{test_file_path}'.")
        print("\n--- RefactoringAgent: Dummy Test Complete ---")


# ==============================================================================
# Local Test Block
# ==============================================================================
if __name__ == "__main__":
    refactoring_agent = RefactoringAgent()
    refactoring_agent.run_dummy_test()
