# Aegis Code Modernization Constitution
## High-Level Goal
The primary objective is to modernize this Python 2 codebase to be fully compatible with Python 3.11. The final code should be clean, efficient, and follow modern best practices.

## Modernization Rules & Style Guide
- IMPORTANT: All print statements must be converted to print() functions.

- All classes must inherit from object to become new-style classes.

- All code must be formatted with black before being considered complete.

- All new functions and methods must include Google-style docstrings with type hints.

## Critical Files
The following files are critical to the application's core logic. Changes here should be carefully planned and tested.

- main.py: This is the application entry point.

## Testing Commands
- The command to run the project's test suite is pytest.

- The agent must ensure all existing and new tests pass after any refactoring
