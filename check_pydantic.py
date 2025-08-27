#!/usr/bin/env python3
"""
Check if Pydantic is available and output the version.
"""

try:
    import pydantic
    with open("pydantic_check.txt", "w") as f:
        f.write("Pydantic is available\n")
        f.write(f"Version: {pydantic.__version__}\n")
except ImportError as e:
    with open("pydantic_check.txt", "w") as f:
        f.write("Pydantic not available\n")
        f.write(f"Error: {e}\n")
