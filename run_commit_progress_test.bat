@echo off
set PYTHONPATH=src
echo Running commit progress manager tests...
python -m pytest tests/code_tests/01_UnitTests/main_modules/test_commit_progress_manager.py -v > test_output.txt 2>&1
echo Test execution completed. Check test_output.txt for results.
