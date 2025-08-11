from project_management.modules.main_modules.task_management import TaskManagement
from project_management.modules.main_modules.progress_report import generate_report

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def main():
    path = "docs/project_management/progress_dashboard.md"
    before = read_file(path)
    print("Content length before update:", len(before))

    tm = TaskManagement()
    tm.generate_wbs_from_idea("Develop Project Management Tool")
    generate_report(tm)

    after = read_file(path)
    print("Content length after update:", len(after))

    if before == after:
        print("No changes detected in progress_dashboard.md after update.")
    else:
        print("progress_dashboard.md updated successfully.")

if __name__ == "__main__":
    main()
