from .task_management import TaskManagement

def main():
    tm = TaskManagement()

    # Titles of 15 important tasks (10 from report + 5 additional subtasks)
    task_titles = [
        "Develop Project Management Tool",
        "Develop Project Management Tool - Subtask Level 1.1",
        "Develop Project Management Tool - Subtask Level 1.3",
        "Develop Project Management Tool - Subtask Level 1.2",
        "Develop Project Management Tool - Subtask Level 2.1.2",
        "Develop Project Management Tool - Subtask Level 2.3.2",
        "Develop Project Management Tool - Subtask Level 2.1.1",
        "Develop Project Management Tool - Subtask Level 2.3.1",
        "Develop Project Management Tool - Subtask Level 2.2.1",
        "Develop Project Management Tool - Subtask Level 2.2.2",
        # Additional 5 subtasks to reach 15
        "Develop Project Management Tool - Subtask Level 3.1.1",
        "Develop Project Management Tool - Subtask Level 3.1.2",
        "Develop Project Management Tool - Subtask Level 3.2.1",
        "Develop Project Management Tool - Subtask Level 3.2.2",
        "Develop Project Management Tool - Subtask Level 3.3.1",
    ]

    # Create tasks
    tasks = []
    for title in task_titles:
        task = tm.parse_creative_input(title)
        tasks.append(task)

    # Mark tasks as completed to simulate "doing" them
    for task in tasks:
        tm.mark_task_completed(task.id)

    # Print summary of completed tasks
    print("Completed 15 important tasks:")
    for task in tasks:
        print(f"Task ID: {task.id}, Title: {task.title}, Status: {task.status}")

if __name__ == "__main__":
    main()
