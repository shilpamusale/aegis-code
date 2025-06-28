import json
from src.agents.code_analysis_agent import analyze_code_structure


def test_analyze_code_with_valid_syntax():
    """
    Tests that the tool correctly analyzes a valid piece of Python code
    and returns a structured JSON summary.
    """
    sample_code = """
import os

class MyClass:
    def my_method(self):
        pass

def my_function():
    pass
"""
    result_json = analyze_code_structure(sample_code)
    result = json.loads(result_json)

    assert "error" not in result
    assert len(result["imports"]) == 1
    assert result["imports"][0]["module"] == "os"

    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "MyClass"
    assert len(result["classes"][0]["methods"]) == 1
    assert result["classes"][0]["methods"][0]["name"] == "my_method"

    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "my_function"


def test_analyze_code_with_syntax_error():
    """
    Tests that the tool gracefully handles invalid Python code
    and returns a JSON object containing an error message.
    """
    invalid_code = "def invalid function()"
    result_json = analyze_code_structure(invalid_code)
    result = json.loads(result_json)

    assert "error" in result
    assert result["error"] == "Invalid Python syntax"
