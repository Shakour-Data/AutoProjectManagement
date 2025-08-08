import argparse
import os
import subprocess
import logging
from ..main_modules.setup_initialization import initialize_git_repo, create_virtualenv, install_dependencies, create_requirements_file, ensure_gitignore_excludes_venv

logger = logging.getLogger("cli_commands")
logging.basicConfig(level=logging.INFO)

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command {command} failed with error: {e}")

def prompt_user(question, default=None):
    prompt = f"{question}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    response = input(prompt)
    if not response and default is not None:
        return default
    return response

def setup_project():
    import shutil
    import os

    logger.info("Starting project setup...")

    # Remove PM_UserInputs folder if it exists
    pm_userinputs_path = os.path.join(os.getcwd(), 'PM_UserInputs')
    if os.path.exists(pm_userinputs_path) and os.path.isdir(pm_userinputs_path):
        shutil.rmtree(pm_userinputs_path)
        logger.info("Removed obsolete PM_UserInputs directory.")

    # Initialize git repo
    initialize_git_repo()

    # Ensure .gitignore excludes venv
    ensure_gitignore_excludes_venv()

    # Create requirements.txt
    create_requirements_file()

    # Create virtual environment
    create_virtualenv()

    # Install dependencies
    install_dependencies()

    logger.info("\nSetup complete.")
    logger.info("Please add your project dependencies to requirements.txt if not already done.")
    logger.info("Place your JSON input files in the 'project_inputs/PM_JSON/user_inputs' directory.")
    logger.info("You can then proceed with other commands.")

def status():
    logger.info("Project Management Tool Status:")
    if os.path.exists('.git'):
        logger.info("- Git repository initialized.")
    else:
        logger.info("- Git repository not found.")
    if os.path.exists('venv'):
        logger.info("- Virtual environment exists.")
    else:
        logger.info("- Virtual environment not found.")
    if os.path.exists('requirements.txt'):
        logger.info("- requirements.txt file exists.")
    else:
        logger.info("- requirements.txt file not found.")
    if os.path.exists('project_inputs/PM_JSON/user_inputs'):
        logger.info("- project_inputs/PM_JSON/user_inputs directory exists.")
    else:
        logger.info("- project_inputs/PM_JSON/user_inputs directory not found.")

def main():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    parser.add_argument('command', nargs='?', help='Command to run: setup, status, etc.')

    args = parser.parse_args()

    if args.command == 'setup':
        setup_project()
    elif args.command == 'status':
        status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
