# Project Management Package Scenarios

*Last updated: 2025-07-27*

This document defines all possible scenarios for the ProjectManagement system, providing a comprehensive overview of the package's usage, setup, planning, execution, and monitoring processes.

## 1. Initial Setup and Installation

1. The user creates an empty project folder.
2. The ProjectManagement package is installed into the project folder.
3. The package files and folders are not tracked by the user's project Git repository.
4. A Git repository is initialized in the project folder.
5. Essential files such as `requirements.txt`, `.gitignore`, and `README.md` are created.
6. A `Docs` folder is created for project documentation.
7. A Python virtual environment is created within the project folder.
8. Virtual environment files and folders are excluded from Git tracking.
9. The required Python packages listed in `requirements.txt` are installed.
10. The system instructs the user to add JSON files for the Work Breakdown Structure (WBS) parts under the directory:  
    `SystemInputs/user_inputs/wbs_parts`
11. The user must add three levels of WBS parts to plan the project.
12. The system lists the expected JSON filenames and paths one by one.
13. The user completes each JSON file according to the provided standards and confirms by pressing Enter.
14. The system validates each JSON file against general and package-specific standards before proceeding to the next file.
15. The user defines the human resources JSON file as per the system's instructions and standards.

## 2. Project Planning and Scheduling

1. The system performs resource allocation for the lowest-level WBS activities (tasks) based on the user-defined human resources.
2. The system estimates the duration (in hours) for each activity.
3. The system determines the dependencies (predecessors and successors) for each activity.

   * It adds a start milestone activity for activities without predecessors (project start).
   * It adds an end milestone activity for activities without successors (project end).

4. The system performs resource leveling to optimize resource usage.
5. The user provides the project start date.
6. The system calculates the start and end dates for each activity.
7. Starting from the lowest WBS level, the system aggregates durations, costs, and other calculations up to higher levels.
8. The system announces that the initial project schedule is created, including total project duration and cost (human resource cost only).
9. The system generates various dashboards and reports for the initial project plan.
10. The system provides filtering and sorting capabilities for activities and higher WBS levels based on all scheduling attributes.

## 3. Project Monitoring and Control

1. During project execution, the package monitors the project by:

   * Determining priority, importance, and scores for activities and aggregating these to higher WBS levels.
   * If two activities have the same priority and importance, the one in a group with higher priority and importance receives a higher score.
   * Determining the order of activities and managing their execution by team members.
   * Generating dashboards and reports related to activity execution.
   * Managing workflow for activities designated for execution.
   * Creating commits after completing workflow parts and updating project progress percentage.
   * Generating all relevant reports at the end of each workday (e.g., 6 PM daily).
   * Updating dashboards after each commit.
   * Checking if the workflow is complete:
     * If yes, return to priority determination step.
     * If no, continue workflow execution.

## 4. Notes

* All user inputs must comply with the package's JSON standards and formats.
* The system guides the user through each step, providing instructions and validation feedback.
* The package does not use AI for any of the above processes.
* The package focuses on automation, consistency, and adherence to project management best practices.

---

This document replaces any previous AI-based automation with a user-interactive, standards-driven project management process.
