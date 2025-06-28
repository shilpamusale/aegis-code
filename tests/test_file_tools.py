# In src/tests/test_file_tools.py

from src.agents.refactoring_agent import read_file, write_file


def test_write_and_read_file(tmp_path):
    """
    Tests the write_file and read_file tools in a successful scenario.
    It writes content to a temporary file and then reads it back to
    ensure the content matches.

    Args:
        tmp_path: A pytest fixture that provides a temporary directory path.
    """
    file_path = tmp_path / "test_file.txt"
    content_to_write = "Hello, Aegis Code!"

    # Test writing the file
    write_result = write_file(str(file_path), content_to_write)
    assert "Successfully wrote" in write_result
    assert file_path.exists()

    # Test reading the file
    read_content = read_file(str(file_path))
    assert read_content == content_to_write


def test_read_nonexistent_file():
    """
    Tests that the read_file tool correctly handles a scenario
    where the file does not exist, returning an error message.
    """
    read_result = read_file("non_existent_file_12345.txt")
    assert "Error: File not found" in read_result
