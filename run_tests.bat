@echo off
echo Running tests...
python -m pytest tests/code_tests/01_UnitTests/api/test_auth_models.py -v > test_output.txt 2>&1
echo Test execution completed. Check test_output.txt for results.
