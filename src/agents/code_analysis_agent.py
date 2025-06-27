# In src/agents/code_analysis_agent.py

import ast
import json
from typing import Any, Dict, List, Set


class CodeVisitor(ast.NodeVisitor):
    """
    Walks the Abstract Syntax Tree of Python code to extract structural info.

    This class visits each node of the parsed tree and collects details about
    classes, functions, imports, and global variables.
    """

    def __init__(self) -> None:
        self.structure: Dict[str, List[Dict[str, Any]]] = {
            "imports": [],
            "classes": [],
            "functions": [],
        }
        self.imported_names: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        """Extracts standard imports (e.g., import os)."""
        for alias in node.names:
            self.structure["imports"].append(
                {
                    "module": alias.name,
                    "as": alias.asname,
                }
            )
            self.imported_names.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Extracts 'from' imports (e.g., from os import path)."""
        module = node.module or ""
        for alias in node.names:
            self.structure["imports"].append(
                {
                    "module": f"{module}.{alias.name}",
                    "as": alias.asname,
                }
            )
            self.imported_names.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Extracts class definitions, including their methods."""
        class_info = {
            "name": node.name,
            "methods": [],
            "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
        }
        # Visit methods within the class
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._get_function_info(item)
                class_info["methods"].append(method_info)
        self.structure["classes"].append(class_info)
        # We don't call generic_visit to avoid double-counting methods as global functions

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extracts top-level function definitions."""
        # This check ensures we only capture top-level functions, not methods inside classes.
        if not hasattr(node, "parent") or not isinstance(node.parent, ast.ClassDef):
            self.structure["functions"].append(self._get_function_info(node))
        # We still call generic_visit to traverse into nested functions if any.
        self.generic_visit(node)

    def _get_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Helper to extract common information from functions and methods."""
        return {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "docstring": ast.get_docstring(node),
        }


def analyze_code_structure(code: str) -> str:
    """
    Analyzes a string of Python code and returns its structure as a JSON string.

    This function serves as the primary tool for the CodeAnalysisAgent. It uses
    the AST library to create a reliable, structured representation of the code.

    Args:
        code: A string containing valid Python source code.

    Returns:
        A JSON string summarizing the code's structure. Returns an error
        message in JSON format if the code cannot be parsed.
    """
    try:
        tree = ast.parse(code)
        # Pre-process the tree to add parent pointers for accurate context.
        # This is crucial for distinguishing methods from top-level functions.
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        visitor = CodeVisitor()
        visitor.visit(tree)
        return json.dumps(visitor.structure, indent=2)
    except SyntaxError as e:
        return json.dumps(
            {"error": "Invalid Python syntax", "details": str(e)}, indent=2
        )


class CodeAnalysisAgent:
    """
    An agent specialized in analyzing and understanding code structure.
    """

    def __init__(self):
        self.tool = analyze_code_structure

    def run(self, code_to_analyze: str) -> str:
        """
        Executes the agent's primary function: analyzing code.
        """
        print("--- CodeAnalysisAgent: Analyzing code... ---")
        analysis_json = self.tool(code_to_analyze)
        print(analysis_json)
        print("--- CodeAnalysisAgent: Analysis complete. ---")
        return analysis_json


# ==============================================================================
# Local Test Block
# ==============================================================================
if __name__ == "__main__":
    # Sample Python code to test the analysis
    sample_code = """
import os
from typing import List

class MyCoolClass:
    \"\"\"This is a sample class.\"\"\"
    def __init__(self, name):
        self.name = name

    def greet(self):
        \"\"\"A method to greet.\"\"\"
        print(f"Hello, {self.name}")

def standalone_function(items: List[str]) -> None:
    \"\"\"This is a standalone function.\"\"\"
    for item in items:
        print(item)
"""

    # Create an instance of the agent and run the analysis
    analysis_agent = CodeAnalysisAgent()
    analysis_agent.run(sample_code)
