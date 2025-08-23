import argparse
import os
import subprocess
import logging
import json
from autoprojectmanagement.main_modules.utility_modules.setup_initialization import initialize_git_repo, create_virtualenv, install_dependencies, create_requirements_file, ensure_gitignore_excludes_venv
from autoprojectmanagement.services.integration_services.github_project_manager import GitHubProjectManager

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

def create_github_project(args):
    """Create a new GitHub project with full integration"""
    manager = GitHubProjectManager()
    
    project_name = args.project_name
    description = args.description or ""
    github_username = args.github_username
    
    if not github_username:
        github_username = input("Enter your GitHub username: ")
    
    print(f"🚀 Creating GitHub project '{project_name}'...")
    
    try:
        reports = manager.create_github_project_cli(project_name, description, github_username)
        
        print("\n✅ GitHub project created successfully!")
        print(f"📊 Repository: https://github.com/{github_username}/{project_name}")
        print(f"📋 Project Board: https://github.com/{github_username}/{project_name}/projects")
        print(f"📝 Issues: https://github.com/{github_username}/{project_name}/issues")
        
        # Save detailed report
        reports_dir = "github_reports"
        os.makedirs(reports_dir, exist_ok=True)
        report_file = os.path.join(reports_dir, f"{project_name}_setup_report.json")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
    except Exception as e:
        logger.error(f"Failed to create GitHub project: {e}")
        print(f"❌ Error: {e}")

def sync_with_github(args):
    """Sync existing project with GitHub"""
    manager = GitHubProjectManager()
    
    project_json = args.project_json
    github_username = args.github_username
    
    if not os.path.exists(project_json):
        logger.error(f"Project JSON file not found: {project_json}")
        return
    
    try:
        reports = manager.create_github_project_from_json(project_json, github_username)
        
        print("\n✅ Project synced with GitHub successfully!")
        print(f"📄 Reports saved to github_reports directory")
        
    except Exception as e:
        logger.error(f"Failed to sync project with GitHub: {e}")
        print(f"❌ Error: {e}")

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
    if os.path.exists('github_reports'):
        logger.info("- GitHub reports directory exists.")
    else:
        logger.info("- GitHub reports directory not found.")

def main():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Setup the project environment')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check project status')
    
    # Create GitHub project command
    github_parser = subparsers.add_parser('create-github', help='Create GitHub project with full integration')
    github_parser.add_argument('project_name', help='Name of the GitHub project')
    github_parser.add_argument('--description', help='Project description')
    github_parser.add_argument('--github-username', help='GitHub username (optional)')
    
    # Sync with GitHub command
    sync_parser = subparsers.add_parser('sync-github', help='Sync existing project with GitHub')
    sync_parser.add_argument('project_json', help='Path to project JSON file')
    sync_parser.add_argument('github_username', help='GitHub username')
    
    args = parser.parse_args()

    if args.command == 'setup':
        setup_project()
    elif args.command == 'status':
        status()
    elif args.command == 'create-github':
        create_github_project(args)
    elif args.command == 'sync-github':
        sync_with_github(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
